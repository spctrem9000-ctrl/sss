class Product {
  final int id;
  final int categoryId;
  final String nameAr;
  final String nameEn;
  final String? descriptionAr;
  final String? descriptionEn;
  final String? image;
  final bool isAvailable;
  final bool isFeatured;
  final bool isHidden;
  final bool isOffer;
  final bool hasSizes;
  final bool hasAddons;
  final double basePrice;
  final int? preparationTime;
  final int? calories;
  final int sortOrder;

  Product({
    required this.id,
    required this.categoryId,
    required this.nameAr,
    required this.nameEn,
    this.descriptionAr,
    this.descriptionEn,
    this.image,
    required this.isAvailable,
    required this.isFeatured,
    required this.isHidden,
    required this.isOffer,
    required this.hasSizes,
    required this.hasAddons,
    required this.basePrice,
    this.preparationTime,
    this.calories,
    required this.sortOrder,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      categoryId: json['category_id'],
      nameAr: json['name_ar'],
      nameEn: json['name_en'],
      descriptionAr: json['description_ar'],
      descriptionEn: json['description_en'],
      image: json['image'],
      isAvailable: json['is_available'] ?? true,
      isFeatured: json['is_featured'] ?? false,
      isHidden: json['is_hidden'] ?? false,
      isOffer: json['is_offer'] ?? false,
      hasSizes: json['has_sizes'] ?? false,
      hasAddons: json['has_addons'] ?? false,
      basePrice: (json['base_price'] as num).toDouble(),
      preparationTime: json['preparation_time'],
      calories: json['calories'],
      sortOrder: json['sort_order'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'category_id': categoryId,
      'name_ar': nameAr,
      'name_en': nameEn,
      'description_ar': descriptionAr,
      'description_en': descriptionEn,
      'image': image,
      'is_available': isAvailable,
      'is_featured': isFeatured,
      'is_hidden': isHidden,
      'is_offer': isOffer,
      'has_sizes': hasSizes,
      'has_addons': hasAddons,
      'base_price': basePrice,
      'preparation_time': preparationTime,
      'calories': calories,
      'sort_order': sortOrder,
    };
  }
}
