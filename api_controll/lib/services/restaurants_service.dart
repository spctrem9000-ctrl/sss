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
    String currency = "SAR",
    String country = "SA",
    bool isEnabled = true,
  }) async {
    final response = await _api.post('/admin/restaurants', {
      'name': name,
      'currency': currency,
      'country': country,
      'is_enabled': isEnabled,
    });
    
    return Restaurant.fromJson(response);
  }

  Future<Restaurant> updateRestaurant(int id, {bool? isEnabled}) async {
    final Map<String, dynamic> data = {};
    if (isEnabled != null) data['is_enabled'] = isEnabled;
    
    final response = await _api.patch('/admin/restaurants/$id', data);
    return Restaurant.fromJson(response);
  }
}
