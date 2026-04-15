from app.cache_keys import project_summary_cache_key


def get_project_summary(tenant_id, project_slug, datastore, cache):
    key = project_summary_cache_key(project_slug)
    cached = cache.get(key)
    if cached is not None:
        return cached

    summary = datastore[(tenant_id, project_slug)]
    result = {
        "tenant_id": tenant_id,
        "project_slug": project_slug,
        "summary": summary,
    }
    cache.set(key, result)
    return result
