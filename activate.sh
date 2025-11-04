#!/bin/bash
# TMS Project Activation Script
# This script activates the virtual environment and provides helpful commands

echo "🚀 Activating TMS Virtual Environment..."
source venv/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "📋 Available commands:"
echo "  python manage.py runserver     - Start development server"
echo "  python manage.py migrate       - Apply database migrations"
echo "  python manage.py makemigrations - Create new migrations"
echo "  python manage.py createsuperuser - Create admin user"
echo "  python manage.py populate_sample_data - Add sample data"
echo "  python manage.py shell         - Open Django shell"
echo ""
echo "🌐 Admin Interface: http://127.0.0.1:8000/admin/"
echo "👤 Admin Credentials: admin / admin123"
echo ""
echo "💡 To deactivate: type 'deactivate'"
echo ""
