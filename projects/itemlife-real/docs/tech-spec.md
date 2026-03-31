# 技术方案书 - 物品寿命App (真实项目)

**项目**: ItemLife  
**环节**: 3/6 - 技术方案  
**状态**: 🔧 详细设计中  
**版本**: v1.0  
**日期**: 2026-03-24

---

## 1. 技术架构总览

### 1.1 分层架构

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Screens                                         │   │
│  │  ├── home_screen.dart                           │   │
│  │  ├── add_item_screen.dart                       │   │
│  │  ├── item_detail_screen.dart                    │   │
│  │  ├── stats_screen.dart                          │   │
│  │  └── settings_screen.dart                       │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Widgets                                         │   │
│  │  ├── item_card.dart                             │   │
│  │  ├── lifespan_bar.dart                          │   │
│  │  ├── primary_button.dart                        │   │
│  │  └── input_field.dart                           │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Providers (Riverpod)                            │   │
│  │  ├── item_providers.dart                        │   │
│  │  └── settings_providers.dart                    │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                     Domain Layer                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Models                                          │   │
│  │  ├── item.dart                                  │   │
│  │  ├── category.dart                              │   │
│  │  └── statistics.dart                            │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Repositories (Abstract)                         │   │
│  │  └── item_repository.dart                       │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Services (Abstract)                             │   │
│  │  ├── notification_service.dart                  │   │
│  │  └── analytics_service.dart                     │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                      Data Layer                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Local Data Source                               │   │
│  │  ├── item_local_source.dart                     │   │
│  │  └── hive_adapters.dart                         │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Remote Data Source (Optional)                   │   │
│  │  └── firebase_service.dart                      │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Repository Implementations                      │   │
│  │  └── item_repository_impl.dart                  │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                   Core Layer                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Constants                                       │   │
│  │  ├── colors.dart                                │   │
│  │  ├── typography.dart                            │   │
│  │  └── spacing.dart                               │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Utils                                           │   │
│  │  ├── date_utils.dart                            │   │
│  │  └── validators.dart                            │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Extensions                                      │   │
│  │  └── date_extension.dart                        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 1.2 技术选型

| 层级 | 技术 | 版本 | 理由 |
|------|------|------|------|
| **Flutter SDK** | Flutter | 3.19+ | 跨平台，开发效率高 |
| **状态管理** | Riverpod | 2.x | 类型安全，依赖注入 |
| **路由** | GoRouter | 13.x | 声明式路由，深度链接 |
| **本地存储** | Hive | 2.x | 高性能NoSQL，对象存储 |
| **代码生成** | Freezed | 2.x | 不可变对象，JSON序列化 |
| **通知** | Flutter Local Notifications | 16.x | 本地通知，无需后端 |
| **图表** | fl_chart | 0.66 | 轻量图表库 |
| **图片选择** | image_picker | 1.x | 系统相册/相机 |
| **权限** | permission_handler | 11.x | 权限管理 |

---

## 2. 数据模型设计

### 2.1 Item 模型

```dart
// lib/domain/models/item.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hive_flutter/hive_flutter.dart';

part 'item.freezed.dart';
part 'item.g.dart';

@HiveType(typeId: 0)
@freezed
class Item with _$Item {
  const factory Item({
    @HiveField(0) required String id,
    @HiveField(1) required String name,
    @HiveField(2) required String category,
    @HiveField(3) required DateTime purchaseDate,
    @HiveField(4) required double price,
    @HiveField(5) required int expectedLifespanMonths,
    @HiveField(6) String? imagePath,
    @HiveField(7) String? notes,
    @HiveField(8) @Default(false) bool isArchived,
    @HiveField(9) required DateTime createdAt,
    @HiveField(10) required DateTime updatedAt,
  }) = _Item;

  const Item._();

  factory Item.fromJson(Map<String, dynamic> json) => _$ItemFromJson(json);

  /// 创建新物品工厂方法
  factory Item.create({
    required String name,
    required String category,
    required DateTime purchaseDate,
    required double price,
    required int expectedLifespanMonths,
    String? imagePath,
    String? notes,
  }) {
    final now = DateTime.now();
    return Item(
      id: now.millisecondsSinceEpoch.toString(),
      name: name,
      category: category,
      purchaseDate: purchaseDate,
      price: price,
      expectedLifespanMonths: expectedLifespanMonths,
      imagePath: imagePath,
      notes: notes,
      createdAt: now,
      updatedAt: now,
    );
  }

  // ========== 计算字段 ==========

  /// 已使用月数
  int get usedMonths {
    final now = DateTime.now();
    return (now.year - purchaseDate.year) * 12 + 
           (now.month - purchaseDate.month);
  }

  /// 已使用天数
  int get usedDays {
    return DateTime.now().difference(purchaseDate).inDays;
  }

  /// 剩余月数
  int get remainingMonths => expectedLifespanMonths - usedMonths;

  /// 剩余天数
  int get remainingDays => remainingMonths * 30; // 估算

  /// 日均成本
  double get dailyCost {
    if (usedDays <= 0) return price;
    return price / usedDays;
  }

  /// 预计到期日期
  DateTime get expiryDate {
    return DateTime(
      purchaseDate.year,
      purchaseDate.month + expectedLifespanMonths,
      purchaseDate.day,
    );
  }

  /// 使用进度百分比 (0.0 - 1.0)
  double get progressPercent {
    final percent = usedMonths / expectedLifespanMonths;
    return percent.clamp(0.0, 1.0);
  }

  /// 剩余百分比
  double get remainingPercent => 1.0 - progressPercent;

  /// 是否即将到期 (剩余 < 30天)
  bool get isExpiringSoon => remainingMonths <= 1;

  /// 是否已过期
  bool get isExpired => remainingMonths <= 0;

  /// 状态颜色
  String get statusColor {
    if (isExpired) return 'expired';
    if (remainingPercent <= 0.25) return 'critical';
    if (remainingPercent <= 0.5) return 'warning';
    return 'healthy';
  }
}
```

### 2.2 Category 枚举

```dart
// lib/domain/models/category.dart
import 'package:flutter/material.dart';

enum ItemCategory {
  electronics('数码', Icons.devices),
  clothing('衣物', Icons.checkroom),
  furniture('家具', Icons.chair),
  appliance('家电', Icons.kitchen),
  books('书籍', Icons.book),
  beauty('美妆', Icons.face),
  sports('运动', Icons.sports),
  other('其他', Icons.more_horiz);

  final String label;
  final IconData icon;

  const ItemCategory(this.label, this.icon);

  static ItemCategory fromString(String value) {
    return ItemCategory.values.firstWhere(
      (e) => e.name == value || e.label == value,
      orElse: () => ItemCategory.other,
    );
  }
}
```

### 2.3 Statistics 模型

```dart
// lib/domain/models/statistics.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'statistics.freezed.dart';

@freezed
class ItemStatistics with _$ItemStatistics {
  const factory ItemStatistics({
    required int totalItems,
    required double totalCost,
    required double averageDailyCost,
    required int expiringSoonCount,
    required int expiredCount,
    required Map<String, int> categoryDistribution,
    required Map<String, double> monthlySpending,
  }) = _ItemStatistics;
}
```

---

## 3. 仓库模式实现

### 3.1 抽象接口

```dart
// lib/domain/repositories/item_repository.dart
import 'package:itemlife/domain/models/item.dart';

abstract class ItemRepository {
  /// 获取所有物品
  Future<List<Item>> getAllItems();

  /// 获取单个物品
  Future<Item?> getItemById(String id);

  /// 添加物品
  Future<void> addItem(Item item);

  /// 更新物品
  Future<void> updateItem(Item item);

  /// 删除物品
  Future<void> deleteItem(String id);

  /// 获取即将到期的物品
  Future<List<Item>> getExpiringItems();

  /// 获取已过期物品
  Future<List<Item>> getExpiredItems();

  /// 按分类获取物品
  Future<List<Item>> getItemsByCategory(String category);

  /// 监听所有物品变化
  Stream<List<Item>> watchAllItems();

  /// 搜索物品
  Future<List<Item>> searchItems(String query);

  /// 导出数据为CSV
  Future<String> exportToCsv();

  /// 从CSV导入
  Future<void> importFromCsv(String csvContent);
}
```

### 3.2 本地数据源

```dart
// lib/data/datasources/local/item_local_source.dart
import 'package:hive_flutter/hive_flutter.dart';
import 'package:itemlife/domain/models/item.dart';

class ItemLocalDataSource {
  static const String _boxName = 'items';
  late Box<Item> _box;

  Future<void> init() async {
    _box = await Hive.openBox<Item>(_boxName);
  }

  Future<List<Item>> getAllItems() async {
    return _box.values.toList()
      ..sort((a, b) => a.remainingMonths.compareTo(b.remainingMonths));
  }

  Future<Item?> getItemById(String id) async {
    return _box.get(id);
  }

  Future<void> addItem(Item item) async {
    await _box.put(item.id, item);
  }

  Future<void> updateItem(Item item) async {
    await _box.put(item.id, item.copyWith(updatedAt: DateTime.now()));
  }

  Future<void> deleteItem(String id) async {
    await _box.delete(id);
  }

  Future<void> clearAll() async {
    await _box.clear();
  }

  Stream<List<Item>> watchAllItems() {
    return _box.watch().map((_) => _box.values.toList()
      ..sort((a, b) => a.remainingMonths.compareTo(b.remainingMonths)));
  }

  Future<List<Item>> search(String query) async {
    final lowerQuery = query.toLowerCase();
    return _box.values
        .where((item) =>
            item.name.toLowerCase().contains(lowerQuery) ||
            item.category.toLowerCase().contains(lowerQuery) ||
            (item.notes?.toLowerCase().contains(lowerQuery) ?? false))
        .toList();
  }
}
```

### 3.3 仓库实现

```dart
// lib/data/repositories/item_repository_impl.dart
import 'package:itemlife/data/datasources/local/item_local_source.dart';
import 'package:itemlife/domain/models/item.dart';
import 'package:itemlife/domain/repositories/item_repository.dart';

class ItemRepositoryImpl implements ItemRepository {
  final ItemLocalDataSource _localDataSource;

  ItemRepositoryImpl(this._localDataSource);

  @override
  Future<List<Item>> getAllItems() async {
    return _localDataSource.getAllItems();
  }

  @override
  Future<Item?> getItemById(String id) async {
    return _localDataSource.getItemById(id);
  }

  @override
  Future<void> addItem(Item item) async {
    await _localDataSource.addItem(item);
  }

  @override
  Future<void> updateItem(Item item) async {
    await _localDataSource.updateItem(item);
  }

  @override
  Future<void> deleteItem(String id) async {
    await _localDataSource.deleteItem(id);
  }

  @override
  Future<List<Item>> getExpiringItems() async {
    final items = await _localDataSource.getAllItems();
    return items.where((item) => item.isExpiringSoon && !item.isExpired).toList();
  }

  @override
  Future<List<Item>> getExpiredItems() async {
    final items = await _localDataSource.getAllItems();
    return items.where((item) => item.isExpired).toList();
  }

  @override
  Future<List<Item>> getItemsByCategory(String category) async {
    final items = await _localDataSource.getAllItems();
    return items.where((item) => item.category == category).toList();
  }

  @override
  Stream<List<Item>> watchAllItems() {
    return _localDataSource.watchAllItems();
  }

  @override
  Future<List<Item>> searchItems(String query) async {
    return _localDataSource.search(query);
  }

  @override
  Future<String> exportToCsv() async {
    final items = await _localDataSource.getAllItems();
    final buffer = StringBuffer();
    buffer.writeln('name,category,purchaseDate,price,expectedLifespanMonths,notes');
    for (final item in items) {
      buffer.writeln(
        '${item.name},${item.category},${item.purchaseDate.toIso8601String()},'
        '${item.price},${item.expectedLifespanMonths},${item.notes ?? ''}',
      );
    }
    return buffer.toString();
  }

  @override
  Future<void> importFromCsv(String csvContent) async {
    final lines = csvContent.split('\n');
    for (var i = 1; i < lines.length; i++) {
      if (lines[i].trim().isEmpty) continue;
      final parts = lines[i].split(',');
      if (parts.length >= 5) {
        final item = Item.create(
          name: parts[0],
          category: parts[1],
          purchaseDate: DateTime.parse(parts[2]),
          price: double.parse(parts[3]),
          expectedLifespanMonths: int.parse(parts[4]),
          notes: parts.length > 5 ? parts[5] : null,
        );
        await _localDataSource.addItem(item);
      }
    }
  }
}
```

---

## 4. 状态管理 (Riverpod)

### 4.1 Providers

```dart
// lib/presentation/providers/item_providers.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:itemlife/data/datasources/local/item_local_source.dart';
import 'package:itemlife/data/repositories/item_repository_impl.dart';
import 'package:itemlife/domain/models/item.dart';
import 'package:itemlife/domain/repositories/item_repository.dart';

// 数据源Provider
final itemLocalDataSourceProvider = Provider<ItemLocalDataSource>((ref) {
  return ItemLocalDataSource();
});

// 仓库Provider
final itemRepositoryProvider = Provider<ItemRepository>((ref) {
  final localSource = ref.watch(itemLocalDataSourceProvider);
  return ItemRepositoryImpl(localSource);
});

// 所有物品Stream
final itemsStreamProvider = StreamProvider<List<Item>>((ref) {
  final repository = ref.watch(itemRepositoryProvider);
  return repository.watchAllItems();
});

// 即将到期物品
final expiringItemsProvider = FutureProvider<List<Item>>((ref) async {
  final repository = ref.watch(itemRepositoryProvider);
  return repository.getExpiringItems();
});

// 已过期物品
final expiredItemsProvider = FutureProvider<List<Item>>((ref) async {
  final repository = ref.watch(itemRepositoryProvider);
  return repository.getExpiredItems();
});

// 统计数据
final statisticsProvider = FutureProvider<ItemStatistics>((ref) async {
  final repository = ref.watch(itemRepositoryProvider);
  final items = await repository.getAllItems();
  
  // 计算统计数据...
  return ItemStatistics(
    totalItems: items.length,
    totalCost: items.fold(0, (sum, item) => sum + item.price),
    averageDailyCost: items.isEmpty ? 0 : 
      items.fold(0.0, (sum, item) => sum + item.dailyCost) / items.length,
    expiringSoonCount: items.where((i) => i.isExpiringSoon && !i.isExpired).length,
    expiredCount: items.where((i) => i.isExpired).length,
    categoryDistribution: {},
    monthlySpending: {},
  );
});

// 当前选中物品
final selectedItemProvider = StateProvider<Item?>((ref) => null);
```

---

## 5. 路由配置 (GoRouter)

```dart
// lib/router/app_router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      name: 'home',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/add',
      name: 'add',
      builder: (context, state) => const AddItemScreen(),
    ),
    GoRoute(
      path: '/item/:id',
      name: 'itemDetail',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return ItemDetailScreen(itemId: id);
      },
    ),
    GoRoute(
      path: '/stats',
      name: 'stats',
      builder: (context, state) => const StatsScreen(),
    ),
    GoRoute(
      path: '/settings',
      name: 'settings',
      builder: (context, state) => const SettingsScreen(),
    ),
  ],
);
```

---

## 6. 本地通知服务

```dart
// lib/services/notification_service.dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  final FlutterLocalNotificationsPlugin _notifications = 
      FlutterLocalNotificationsPlugin();

  Future<void> init() async {
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings();
    
    await _notifications.initialize(
      const InitializationSettings(
        android: androidSettings,
        iOS: iosSettings,
      ),
    );
  }

  Future<void> scheduleLifespanReminder(
    String itemId,
    String itemName,
    DateTime expiryDate,
  ) async {
    // 提前7天提醒
    final reminderDate = expiryDate.subtract(const Duration(days: 7));
    
    await _notifications.schedule(
      itemId.hashCode,
      '物品即将到期',
      '$itemName 还有7天就到期了，记得准备更换',
      reminderDate,
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'lifespan_reminder',
          '寿命提醒',
          importance: Importance.high,
        ),
        iOS: DarwinNotificationDetails(),
      ),
    );
  }

  Future<void> cancelReminder(String itemId) async {
    await _notifications.cancel(itemId.hashCode);
  }
}
```

---

## 7. 依赖配置

### 7.1 pubspec.yaml

```yaml
name: itemlife
description: 极简物品寿命管理工具

publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # 状态管理
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3
  
  # 路由
  go_router: ^13.0.1
  
  # 本地存储
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # 代码生成
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  
  # 通知
  flutter_local_notifications: ^16.3.2
  
  # 图表
  fl_chart: ^0.66.0
  
  # 图片
  image_picker: ^1.0.7
  cached_network_image: ^3.3.1
  
  # 权限
  permission_handler: ^11.1.0
  
  # 路径
  path_provider: ^2.1.1
  path: ^1.8.3
  
  # 国际化
  intl: ^0.19.0
  
  # UI组件
  flutter_slidable: ^3.0.1
  shimmer: ^3.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  
  # 代码生成
  build_runner: ^2.4.7
  freezed: ^2.4.5
  json_serializable: ^6.7.1
  hive_generator: ^2.0.1
  riverpod_generator: ^2.3.9
  go_router_builder: ^2.3.4

flutter:
  uses-material-design: true
  
  fonts:
    - family: PingFang SC
      fonts:
        - asset: assets/fonts/PingFang-Regular.ttf
        - asset: assets/fonts/PingFang-Medium.ttf
          weight: 500
        - asset: assets/fonts/PingFang-Semibold.ttf
          weight: 600
        - asset: assets/fonts/PingFang-Bold.ttf
          weight: 700
```

---

## 8. 开发步骤清单

**原则**: 不设固定时间，完成一步→提交确认→自动下一步

### Step 1: 项目搭建
- [ ] Flutter项目创建
- [ ] 依赖配置（pubspec.yaml）
- [ ] 目录结构初始化
- [ ] 代码生成工具配置

### Step 2: 设计系统
- [ ] 色彩常量（colors.dart）
- [ ] 字体规范（typography.dart）
- [ ] 间距常量（spacing.dart）
- [ ] 主题配置（theme.dart）

### Step 3: 数据层
- [ ] Hive适配器生成
- [ ] 本地数据源实现
- [ ] 仓库接口定义
- [ ] 仓库实现

### Step 4: 核心组件
- [ ] ItemCard组件
- [ ] LifespanBar组件
- [ ] PrimaryButton组件
- [ ] InputField组件

### Step 5: 首页
- [ ] 页面布局
- [ ] 物品列表
- [ ] 统计卡片
- [ ] 即将到期区域

### Step 6: 添加物品
- [ ] 表单布局
- [ ] 图片选择
- [ ] 分类选择器
- [ ] 日期选择器

### Step 7: 物品详情
- [ ] 详情展示
- [ ] 寿命圆环
- [ ] 成本分析
- [ ] 删除功能

### Step 8: 统计页
- [ ] 概览数据
- [ ] 分类饼图
- [ ] 趋势折线图

### Step 9: 设置页
- [ ] 数据导出
- [ ] 提醒设置
- [ ] 深色模式

### Step 10: 通知服务
- [ ] 本地通知配置
- [ ] 到期提醒逻辑
- [ ] 通知权限处理

### Step 11: 优化发布
- [ ] 性能优化
- [ ] Bug修复
- [ ] App Store准备

---

## 9. 确认记录（环节3/6 - 决策点1）

**状态**: ✅ **已通过**（2026-03-24 16:35）  
**确认人**: 刘总  
**确认内容**:
- [x] 技术选型: Flutter + Riverpod + Hive + GoRouter
- [x] 架构设计: 3层架构（Presentation/Domain/Data）
- [x] 数据模型: Item/Category/Statistics
- [x] 开发计划: 调整为步骤清单（无固定周期）
- [x] **批准启动开发**: 确认进入开发环节

**下一步**: 开发实现（环节4/6）

---

*Tech Architect + Mobile Dev Lead*  
*INSIGHT AI STUDIO*  
*2026-03-24*
