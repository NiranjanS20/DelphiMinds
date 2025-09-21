from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Post, Comment, PeerProfile
from .serializers import PostSerializer, CommentSerializer, PeerProfileSerializer
from skills.models import UserSkill


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id']).select_related('author').all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs['post_id'])


class BenchmarkingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # recompute simple peer scores
        totals = UserSkill.objects.values('user').annotate(total=Sum('level')).order_by('-total')
        rank_map = {}
        for idx, item in enumerate(totals, start=1):
            rank_map[item['user']] = (idx, item['total'] or 0)
        profiles = []
        for user_id, (rank, total) in rank_map.items():
            pp, _ = PeerProfile.objects.get_or_create(user_id=user_id)
            pp.rank = rank
            pp.total_skill_score = total
            pp.save()
            profiles.append(pp)
        data = PeerProfileSerializer(profiles, many=True).data
        return Response(data)




