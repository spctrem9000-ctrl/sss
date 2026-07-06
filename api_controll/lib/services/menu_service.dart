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
      'name_ar': name,
      'name_en': name,
      'sort_order': 0,
      'is_active': true,
    });
    
    return Category.fromJson(response);
  }

  Future<Product> createProduct({
    required int restaurantId,
    required int categoryId,
    required String name,
    required double basePrice,
    String? description,
  }) async {
    final response = await _api.post('/admin/menu/products', {
      'restaurant_id': restaurantId,
      'category_id': categoryId,
      'name_ar': name,
      'name_en': name,
      'base_price': basePrice,
      'description_ar': description,
      'description_en': description,
      'sort_order': 0,
      'is_available': true,
    });
    
    return Product.fromJson(response);
  }

  Future<List<Category>> getCategories(int restaurantId) async {
    final response = await _api.get('/admin/menu/categories?restaurant_id=$restaurantId');
    return (response as List).map((e) => Category.fromJson(e)).toList();
  }

  Future<List<Product>> getProducts(int categoryId) async {
    final response = await _api.get('/admin/menu/products?category_id=$categoryId');
    return (response as List).map((e) => Product.fromJson(e)).toList();
  }
}
