class Category {
  final int id;
  final String nameAr;
  final String nameEn;
  final String? image;
  final int sortOrder;
  final bool isActive;

  Category({
    required this.id,
    required this.nameAr,
    required this.nameEn,
    this.image,
    required this.sortOrder,
    required this.isActive,
  });

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id'],
      nameAr: json['name_ar'],
      nameEn: json['name_en'],
      image: json['image'],
      sortOrder: json['sort_order'] ?? 0,
      isActive: json['is_active'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name_ar': nameAr,
      'name_en': nameEn,
      'image': image,
      'sort_order': sortOrder,
      'is_active': isActive,
    };
  }
}
