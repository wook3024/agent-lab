#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

ROOT = File.expand_path("..", __dir__)
REGISTRY_PATH = File.join(ROOT, "docs", "ASSET_REGISTRY.yaml")

ALLOWED_GROUPS = %w[topologies agents skills model_policies].freeze
ALLOWED_TYPES = %w[topology agent skill model_policy].freeze
ALLOWED_STATUSES = %w[standard pilot conditional deprecated].freeze
REQUIRED_FIELDS = %w[
  asset_id
  asset_type
  status
  owner
  default_on
  last_validated_batch
  evidence
  notes
].freeze

def fail_with(errors)
  errors.each { |error| warn "ERROR: #{error}" }
  exit 1
end

unless File.exist?(REGISTRY_PATH)
  fail_with(["missing registry file: #{REGISTRY_PATH}"])
end

data = YAML.load_file(REGISTRY_PATH)
errors = []

unless data.is_a?(Hash)
  fail_with(["registry root must be a mapping"])
end

unknown_groups = data.keys - ALLOWED_GROUPS
errors << "unknown top-level groups: #{unknown_groups.join(', ')}" unless unknown_groups.empty?

seen_ids = {}

ALLOWED_GROUPS.each do |group|
  next unless data.key?(group)

  entries = data[group]
  unless entries.is_a?(Array)
    errors << "#{group} must be an array"
    next
  end

  entries.each_with_index do |entry, index|
    unless entry.is_a?(Hash)
      errors << "#{group}[#{index}] must be a mapping"
      next
    end

    REQUIRED_FIELDS.each do |field|
      errors << "#{group}[#{index}] missing required field '#{field}'" unless entry.key?(field)
    end

    asset_id = entry["asset_id"]
    next unless asset_id

    if seen_ids.key?(asset_id)
      errors << "duplicate asset_id '#{asset_id}' in #{group} and #{seen_ids[asset_id]}"
    else
      seen_ids[asset_id] = "#{group}[#{index}]"
    end

    asset_type = entry["asset_type"]
    errors << "#{asset_id}: invalid asset_type '#{asset_type}'" unless ALLOWED_TYPES.include?(asset_type)

    status = entry["status"]
    errors << "#{asset_id}: invalid status '#{status}'" unless ALLOWED_STATUSES.include?(status)

    default_on = entry["default_on"]
    errors << "#{asset_id}: default_on must be boolean" unless default_on == true || default_on == false

    evidence = entry["evidence"]
    unless evidence.is_a?(Array) && evidence.all? { |item| item.is_a?(String) && !item.empty? }
      errors << "#{asset_id}: evidence must be a non-empty array of strings"
    end

    last_validated_batch = entry["last_validated_batch"]
    if !last_validated_batch.is_a?(String) || last_validated_batch.strip.empty?
      errors << "#{asset_id}: last_validated_batch must be a non-empty string"
    end

    notes = entry["notes"]
    errors << "#{asset_id}: notes must be a non-empty string" if !notes.is_a?(String) || notes.strip.empty?

    if status == "deprecated" && default_on
      errors << "#{asset_id}: deprecated asset cannot have default_on=true"
    end

    if status == "pilot" && last_validated_batch == "not-yet-validated"
      errors << "#{asset_id}: pilot asset must have a real last_validated_batch value"
    end

    if status == "standard" && !default_on
      errors << "#{asset_id}: standard asset should normally have default_on=true"
    end

    if %w[conditional pilot].include?(status) && entry["decision_gate"].to_s.strip.empty?
      errors << "#{asset_id}: #{status} asset should declare decision_gate"
    end
  end
end

if errors.empty?
  puts "asset-registry-valid"
else
  fail_with(errors)
end
