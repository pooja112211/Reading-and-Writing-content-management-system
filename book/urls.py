
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    

    path('type/', views.type, name='type'),
    path('add_type/', views.add_type, name='add_type'),

    path('novel/', views.novel, name='novel'),
    path('add_novel/', views.add_novel, name='add_novel'),
    path('update_novel/<int:id>/', views.update_novel, name='update_novel'),
    path('view_novel/<int:id>/', views.view_novel, name='view_novel'),
    path('delete_novel/<int:id>/', views.delete_novel, name='delete_novel'),

    path('series/', views.series, name='series'),
    path('add_series/', views.add_series, name='add_series'),
    path('movies/', views.movies, name='movies'),
    path('add_movies/', views.add_movies, name='add_movies'),

    path('category/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/<int:id>/', views.update_category, name='update_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),

    path('ur_own/', views.ur_own, name='ur_own'),
    path('mine_list/', views.mine_list, name='mine_list'),
    path('mine_list_update/<int:id>/', views.mine_list_update, name='mine_list_update'),
    path('mine_list_delete/<int:id>/', views.mine_list_delete, name='mine_list_delete'),
    path('mine_list_view/<int:id>/', views.mine_list_view, name='mine_list_view'),
    path('download_pdf/<int:id>/', views.download_pdf, name='download_pdf'),

    path('buyer/', views.buyer, name='buyer'),

    # path('items/<int:type_id>/<str:category>/', views.items, name='items'),
  
] + static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
