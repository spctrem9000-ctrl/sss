import '../models/restaurant.dart';
import 'api_client.dart';

class RestaurantsService {
  final ApiClient _api = ApiClient();

  Future<List<Restaurant>> getRestaurants() async {
    final response = await _api.get('/admin/restaurants');
    
    if (response is List) {
      return response.map((json) => Restaurant.fromJson(json)).toList();
    }
    return [];
  }

  Future<Restaurant> createRestaurant({
    required String name,
    required String slug,
    required String description,
    bool isActive = true,
  }) async {
    final response = await _api.post('/admin/restaurants', {
      'name': name,
      'slug': slug,
      'description': description,
      'is_active': isActive,
    });
    
    return Restaurant.fromJson(response);
  }
}
