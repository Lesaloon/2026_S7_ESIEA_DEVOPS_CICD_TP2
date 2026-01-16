"""Performance tests and benchmarks."""
import os
import tempfile
from app.db import init_db, add_user
from app.utils import doThing, GLOBAL


def test_add_user_performance(benchmark):
    """Benchmark user creation performance."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()
        
        def create_user():
            return add_user("Performance Test User")
        
        result = benchmark(create_user)
        assert result is not None


def test_get_user_performance(benchmark):
    """Benchmark user retrieval performance."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()
        
        # Add test user
        user_id = add_user("Perf Test")
        
        def get_user_op():
            from app.db import get_user
            return get_user(user_id)
        
        result = benchmark(get_user_op)
        assert result is not None


def test_dothing_performance(benchmark):
    """Benchmark doThing function performance."""
    GLOBAL["users"].clear()
    
    def do_thing_op():
        return doThing("perf_user", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    
    result = benchmark(do_thing_op)
    assert result is True


def test_dothing_update_performance(benchmark):
    """Benchmark doThing update performance."""
    GLOBAL["users"].clear()
    doThing("existing_user", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    
    def update_thing_op():
        return doThing("existing_user", 10, 20, 30, 40, 50, 60, 70, 80, 90)
    
    result = benchmark(update_thing_op)
    assert result is True
