"""
Management command to set up test users and groups with permissions.

This command creates:
- Three groups: Viewers, Editors, Admins
- Test users assigned to each group
- Permissions assigned to groups based on their roles

Usage:
    python manage.py setup_test_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates test users and groups with appropriate permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing test users and groups before creating new ones',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        reset = options['reset']

        # Get permissions from bookshelf app
        can_view_book = Permission.objects.get(
            codename='can_view_book',
            content_type__app_label='bookshelf'
        )
        can_create_book = Permission.objects.get(
            codename='can_create_book',
            content_type__app_label='bookshelf'
        )
        can_edit_book = Permission.objects.get(
            codename='can_edit_book',
            content_type__app_label='bookshelf'
        )
        can_delete_book = Permission.objects.get(
            codename='can_delete_book',
            content_type__app_label='bookshelf'
        )

        # Get permissions from relationship_app
        can_add_book_rel = Permission.objects.get(
            codename='can_add_book',
            content_type__app_label='relationship_app'
        )
        can_change_book_rel = Permission.objects.get(
            codename='can_change_book',
            content_type__app_label='relationship_app'
        )
        can_delete_book_rel = Permission.objects.get(
            codename='can_delete_book',
            content_type__app_label='relationship_app'
        )

        if reset:
            self.stdout.write(self.style.WARNING('Deleting existing test users and groups...'))
            # Delete test users
            User.objects.filter(
                username__in=['viewer_user', 'editor_user', 'admin_user']
            ).delete()
            # Delete test groups
            Group.objects.filter(
                name__in=['Viewers', 'Editors', 'Admins']
            ).delete()
            self.stdout.write(self.style.SUCCESS('Existing test data deleted.'))

        # Create Groups
        self.stdout.write('Creating groups...')
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        editors_group, created = Group.objects.get_or_create(name='Editors')
        admins_group, created = Group.objects.get_or_create(name='Admins')

        # Assign permissions to groups
        # Viewers: can only view books
        viewers_group.permissions.clear()
        viewers_group.permissions.add(can_view_book)
        self.stdout.write(self.style.SUCCESS(f'✓ Viewers group created with can_view_book permission'))

        # Editors: can view, create, and edit books
        editors_group.permissions.clear()
        editors_group.permissions.add(can_view_book, can_create_book, can_edit_book)
        # Also add relationship_app permissions
        editors_group.permissions.add(can_add_book_rel, can_change_book_rel)
        self.stdout.write(self.style.SUCCESS(
            f'✓ Editors group created with can_view_book, can_create_book, can_edit_book permissions'
        ))

        # Admins: can do everything
        admins_group.permissions.clear()
        admins_group.permissions.add(
            can_view_book, can_create_book, can_edit_book, can_delete_book
        )
        # Also add relationship_app permissions
        admins_group.permissions.add(can_add_book_rel, can_change_book_rel, can_delete_book_rel)
        self.stdout.write(self.style.SUCCESS(
            f'✓ Admins group created with all permissions (view, create, edit, delete)'
        ))

        # Create test users
        self.stdout.write('\nCreating test users...')

        # Viewer user
        viewer_user, created = User.objects.get_or_create(
            username='viewer_user',
            defaults={
                'email': 'viewer@example.com',
                'first_name': 'Viewer',
                'last_name': 'User',
            }
        )
        if created:
            viewer_user.set_password('viewer123')
            viewer_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Created viewer_user (password: viewer123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠ viewer_user already exists, skipping creation'))
        viewer_user.groups.add(viewers_group)

        # Editor user
        editor_user, created = User.objects.get_or_create(
            username='editor_user',
            defaults={
                'email': 'editor@example.com',
                'first_name': 'Editor',
                'last_name': 'User',
            }
        )
        if created:
            editor_user.set_password('editor123')
            editor_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Created editor_user (password: editor123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠ editor_user already exists, skipping creation'))
        editor_user.groups.add(editors_group)

        # Admin user
        admin_user, created = User.objects.get_or_create(
            username='admin_user',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Created admin_user (password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠ admin_user already exists, skipping creation'))
        admin_user.groups.add(admins_group)

        self.stdout.write(self.style.SUCCESS('\n✓ Test users and groups setup completed!'))
        self.stdout.write('\nTest Users:')
        self.stdout.write('  - viewer_user (password: viewer123) - Can only view books')
        self.stdout.write('  - editor_user (password: editor123) - Can view, create, and edit books')
        self.stdout.write('  - admin_user (password: admin123) - Can do everything (view, create, edit, delete)')

