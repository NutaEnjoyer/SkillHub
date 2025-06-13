from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from review.models import Review
from review.serializers import ReviewSerializer


@extend_schema(tags=["Review"])
class ReviewViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing reviews.

    - GET /reviews/: Retrieve a list of all reviews.
    - POST /reviews/: Create a new review.
    - GET /reviews/{id}/: Retrieve a specific review by ID.
    - PUT/PATCH /reviews/{id}/: Update a specific review by ID.
    - DELETE /reviews/{id}/: Delete a specific review by ID.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override the perform_create method to set the user field in the serializer.
        """
        serializer.save(user=self.request.user)
