import '../models/category.dart';
import '../models/product.dart';
import 'api_client.dart';

class MenuService {
  final ApiClient _api = ApiClient();

  Future<Category> createCategory({
    required int restaurantId,
    required String name,
    String? description,
  }) async {
    final response = await _api.post('/admin/menu/categories', {
      'restaurant_id': restaurantId,
      'name': name,
      'description': description,
      'sort_order': 0,
      'is_active': true,
    });
    
    return Category.fromJson(response);
  }

  Future<Product> createProduct({
    required int categoryId,
    required String name,
    required double basePrice,
    String? description,
  }) async {
    final response = await _api.post('/admin/menu/products', {
      'category_id': categoryId,
      'name': name,
      'base_price': basePrice,
      'description': description,
      'sort_order': 0,
      'is_available': true,
    });
    
    return Product.fromJson(response);
  }
}
