import sys

def restore_cursor(console):
    def use_func(func):
        def wrapper(*args, **kwargs):
            try:
                console.show_cursor(False)
                return func(*args, **kwargs)
            finally:
                console.show_cursor(True)
        return wrapper
    return use_func

def swift_exit(console):
    def use_func(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except KeyboardInterrupt:
                console.print("\n[bold dark_red]Checker interrupted by user. Stopping[/bold dark_red]")
                sys.exit(1)
        return wrapper
    return use_func