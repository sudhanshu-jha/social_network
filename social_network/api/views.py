from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,UserSearchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage
from .models import User,FriendRequest
from .serializers import FriendRequestSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Token Obtain Pair View to customize token response data.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Customize the token response data here, if needed
            user = self.user
            # Add any additional data you want to include in the token response
            response.data['user_id'] = user.id
            response.data['username'] = user.username
        return response


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_keyword = request.GET.get('q', '')  # Get the search query parameter 'q' from the URL
        users = User.objects.filter(username__icontains=search_keyword) | User.objects.filter(email__icontains=search_keyword)

        # Implement pagination for search results
        page = request.GET.get('page', 1)
        per_page = 10
        paginator = Paginator(users, per_page)
        try:
            paginated_users = paginator.page(page)
        except EmptyPage:
            paginated_users = paginator.page(paginator.num_pages)

        serializer = UserSearchSerializer(paginated_users, many=True)
        return Response(serializer.data)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, receiver_id):

        sender = request.user
        receiver = User.objects.get(pk=receiver_id)

        # Check if the sender has already sent a request to the receiver
        existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()

        if existing_request:
            return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the sender has sent more than 3 requests within the last minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(sender=sender, timestamp__gte=one_minute_ago).count()

        if recent_requests >= 3:
            return Response({'detail': 'You can send a maximum of 3 friend requests within a minute.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Create a new friend request
        friend_request = FriendRequest(sender=sender, receiver=receiver, status='pending')
        friend_request.save()

        # Serialize the response
        serializer = FriendRequestSerializer(friend_request)

        return Response({'detail': 'Friend request sent successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        # Retrieve the friend request
        friend_request = FriendRequest.objects.get(pk=request_id)

        # Check if the current user is the receiver of the request
        if friend_request.receiver != request.user:
            return Response({'detail': 'You do not have permission to accept this request.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the request status to 'accepted'
        friend_request.status = 'accepted'
        friend_request.save()

        return Response({'detail': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)


class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        # Retrieve the friend request
        friend_request = FriendRequest.objects.get(pk=request_id)

        # Check if the current user is the receiver of the request
        if friend_request.receiver != request.user:
            return Response({'detail': 'You do not have permission to reject this request.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the request status to 'rejected'
        friend_request.status = 'rejected'
        friend_request.save()

        return Response({'detail': 'Friend request rejected successfully.'}, status=status.HTTP_200_OK)


class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        friend_requests = FriendRequest.objects.filter(sender=user, status='accepted')
        friends = [friend.receiver for friend in friend_requests]
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListPendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pending_requests = FriendRequest.objects.filter(receiver=user, status='pending')
        serializer = UserSerializer([request.sender for request in pending_requests], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)