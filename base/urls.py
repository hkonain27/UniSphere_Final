from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # --- Admin ---
    path('admin/', admin.site.urls),

    # --- Authentication ---
    path('accounts/login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),  # Enables login, logout, password reset, etc.
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # --- Main Pages ---
    path('', views.landing_page, name="landing_page"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('about-us/', views.about_us, name="about_us"),
    path('contact-us/', views.contact_us, name="contact_us"),

    # --- Events ---
    path('events/', views.events_page, name="events"),
    path('events/create/', views.create_event, name="create_event"),
    path('events/leave/<int:event_id>/', views.leave_event, name='leave_event'),
    path('events/join/<int:event_id>/', views.join_event, name='join_event'),

    # --- Projects ---
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.add_project, name='add-project'),
    path('projects/comment/<int:project_id>/', views.add_comment, name='add_comment'),
    path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),

    # --- Groups ---
    path('groups/', views.group_discovery, name="group_discovery"),
    path('create-room/', views.create_room, name='create-room'),
    path('groups/join/<int:group_id>/', views.join_group, name="join_group"),
    path('groups/<int:group_id>/chat/', views.group_chat, name="group_chat"),
    path('groups/leave/<int:group_id>/', views.leave_group, name='leave_group'),

    # --- Housing ---
    path('housing/', views.housing_search, name="housing_search"),

    # --- Jobs ---
    path('jobs/', views.job_search, name='job_search'), 
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),

    # --- Profiles ---
    path('profile/<int:pk>/', views.user_profile, name='user-profile'),

    # --- Debug Layout ---
    path('layout/', views.layout, name="layout_test"),
]
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
