import unittest

from app.api import fetch_project_summary
from app.cache import SimpleCache


class TenantCacheScopeTest(unittest.TestCase):
    def test_project_summary_cache_stays_tenant_scoped(self):
        datastore = {
            ("tenant-a", "alpha"): "A summary",
            ("tenant-b", "alpha"): "B summary",
        }
        cache = SimpleCache()

        first = fetch_project_summary(
            {"tenant_id": "tenant-a", "project_slug": "alpha"}, datastore, cache
        )
        second = fetch_project_summary(
            {"tenant_id": "tenant-b", "project_slug": "alpha"}, datastore, cache
        )

        self.assertEqual(first["summary"], "A summary")
        self.assertEqual(second["summary"], "B summary")
        self.assertEqual(second["tenant_id"], "tenant-b")


if __name__ == "__main__":
    unittest.main()
