from django.shortcuts import get_object_or_404
from .models import Category, Movie
from star_ratings.models import Rating, UserRating


def get_ratings(user):
    """Query user UserRating objects based on user and return user ratings."""

    ratings = UserRating.objects.all().filter(user=user)
    user_ratings = []
    for rate in ratings:
        movie = get_object_or_404(Movie, id=rate.rating.object_id)
        categories = movie.category.all()
        user_ratings.append({'movie': movie, 'categories': categories, 'rating': float(rate.rating.average)})

    return user_ratings


def get_recommendations(categories_top, recommendations, rated_movies):
    """Return recommendations based on given categories."""

    for category in categories_top:
        # get top rated movies from category
        top_movies = Movie.objects.filter(ratings__isnull=False).order_by('-ratings__average')
        only_rated = [top_movie.id for top_movie in top_movies if get_object_or_404(Rating,
                                                                                    object_id=top_movie.id).average > 0]
        # only rated movies
        top_movies = top_movies.filter(id__in=only_rated)
        cat_movies = top_movies.filter(category=category)
        # get 5 top rated movies from category
        count = 0
        for mov in cat_movies:
            if mov not in rated_movies and mov not in recommendations:
                if count < 5:
                    recommendations.append(mov)
                    count += 1
    return recommendations


def user_recommendations(user):
    """User recommendations based on most/top rated categories."""

    user_ratings = get_ratings(user)
    rated = [rating.get('movie') for rating in user_ratings]
    recommendations = []
    category_count = {}
    # count ratings by categories
    for movie in user_ratings:
        for category in movie['categories']:
            if category in category_count.keys():
                category_count[category] += 1
            else:
                category_count[category] = 1
    # category top by rated movies quantity
    category_top = sorted(category_count, key=category_count.get, reverse=True)
    recommendations = get_recommendations(category_top[:2], recommendations, rated)
    # count sum of ratings by category
    category_rating = {}
    for movie in user_ratings:
        rate = movie['rating']
        for category in movie['categories']:
            if category in category_rating.keys():
                category_rating[category] += rate
            else:
                category_rating[category] = rate
    # category top by total ratings
    category_top_by_rating = sorted(category_rating, key=category_rating.get, reverse=True)
    recommendations = get_recommendations(category_top_by_rating[:2], recommendations, rated)
    return recommendations
