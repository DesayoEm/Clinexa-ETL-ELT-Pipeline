# ct_gov/include/tests/test_extractor_resilience.py
from ct_gov.include.extractors.extractor import Extractor
from ct_gov.include.tests.failure_generators import FailureGenerator


class ExtractorWithFailureInjection(Extractor):
    """Test-only wrapper that injects failures"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failure_generator = FailureGenerator(True, 0.5)

    def make_requests(self):
        if self.last_saved_page == 3:
            self.failure_generator.maybe_fail_extraction(self.last_saved_page)
        return super().make_requests()