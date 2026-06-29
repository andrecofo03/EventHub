import os
import sys

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subdir = os.path.join(current_dir, 'eventhub')
    if subdir not in sys.path:
        sys.path.insert(0, subdir)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventhub.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
