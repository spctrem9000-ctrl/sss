class Restaurant {
  final int id;
  final String name;
  final bool isEnabled;
  final String? logoUrl;
  final String? themeColor;
  final String currency;
  final String country;
  final String? createdAt;
  final String? updatedAt;

  Restaurant({
    required this.id,
    required this.name,
    required this.isEnabled,
    this.logoUrl,
    this.themeColor,
    required this.currency,
    required this.country,
    this.createdAt,
    this.updatedAt,
  });

  factory Restaurant.fromJson(Map<String, dynamic> json) {
    return Restaurant(
      id: json['id'],
      name: json['name'],
      isEnabled: json['is_enabled'] ?? true,
      logoUrl: json['logo_url'],
      themeColor: json['theme_color'],
      currency: json['currency'] ?? 'SAR',
      country: json['country'] ?? 'SA',
      createdAt: json['created_at'],
      updatedAt: json['updated_at'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'is_enabled': isEnabled,
      'logo_url': logoUrl,
      'theme_color': themeColor,
      'currency': currency,
      'country': country,
      'created_at': createdAt,
      'updated_at': updatedAt,
    };
  }
}
