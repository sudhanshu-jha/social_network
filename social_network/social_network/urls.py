"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import CustomTokenObtainPairView, SignupAPIView , UserSearchAPIView,SendFriendRequestView,AcceptFriendRequestView, RejectFriendRequestView, ListFriendsView,ListPendingRequestsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('user/search/', UserSearchAPIView.as_view(), name='user-search'),
    path('send-friend-request/<int:receiver_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('accept-friend-request/<int:request_id>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('reject-friend-request/<int:request_id>/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('list-friends/', ListFriendsView.as_view(), name='list-friends'),
    path('list-pending-requests/', ListPendingRequestsView.as_view(), name='list-pending-requests'),

]


