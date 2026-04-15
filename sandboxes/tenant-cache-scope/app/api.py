from app.project_summary_service import get_project_summary


def fetch_project_summary(request, datastore, cache):
    tenant_id = request["tenant_id"]
    project_slug = request["project_slug"]
    return get_project_summary(tenant_id, project_slug, datastore, cache)
