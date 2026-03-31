# UI设计规范 - 物品寿命App (真实项目)

**项目**: ItemLife  
**环节**: 2/6 - UI设计  
**状态**: ✅ 已完成（设计规范版）  
**完成时间**: 2026-03-24  
**交付形式**: 详细设计规范文档（非Figma稿）

---

## 1. 设计系统

### 1.1 色彩规范

```dart
// lib/core/constants/colors.dart
class AppColors {
  // 主色调
  static const Color primary = Color(0xFF2C3E50);      // 深蓝灰
  static const Color primaryLight = Color(0xFF34495E); // 灰蓝
  static const Color background = Color(0xFFF8F9FA);   // 浅灰白
  static const Color surface = Color(0xFFFFFFFF);      // 纯白
  
  // 状态色
  static const Color healthy = Color(0xFF27AE60);      // 绿 >75%
  static const Color warning = Color(0xFFF1C40F);      // 黄 50-75%
  static const Color critical = Color(0xFFF39C12);     // 橙 25-50%
  static const Color expired = Color(0xFFE74C3C);      // 红 <25%
  
  // 文字色
  static const Color textPrimary = Color(0xFF212529);   // 近黑
  static const Color textSecondary = Color(0xFF6C757D); // 灰
  static const Color textTertiary = Color(0xFFADB5BD);  // 浅灰
  
  // 功能色
  static const Color divider = Color(0xFFE9ECEF);
  static const Color shadow = Color(0x1A000000);
}
```

### 1.2 字体规范

```dart
// lib/core/constants/typography.dart
class AppTypography {
  // 中文: PingFang SC, 英文: SF Pro
  static const String fontFamily = 'PingFang SC';
  
  // Display - 大标题
  static const TextStyle display = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
  );
  
  // Heading - 页面标题
  static const TextStyle heading = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
  );
  
  // Title - 卡片标题
  static const TextStyle title = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
  );
  
  // Body - 正文
  static const TextStyle body = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.normal,
    color: AppColors.textPrimary,
  );
  
  // Caption - 辅助文字
  static const TextStyle caption = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.normal,
    color: AppColors.textSecondary,
  );
  
  // Small - 标签
  static const TextStyle small = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.normal,
    color: AppColors.textTertiary,
  );
}
```

### 1.3 间距规范

```dart
// lib/core/constants/spacing.dart
class AppSpacing {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double xxl = 48;
  
  // 页面边距
  static const double screenPadding = 16;
  
  // 卡片内边距
  static const double cardPadding = 16;
  
  // 列表间距
  static const double listGap = 12;
}
```

### 1.4 圆角规范

```dart
class AppRadius {
  static const double small = 4;
  static const double medium = 8;
  static const double large = 12;
  static const double xl = 16;
  static const double round = 50; // 圆形/胶囊
}
```

---

## 2. 页面设计详解

### 2.1 首页 (HomeScreen)

**布局结构**:
```
┌─────────────────────────────────────┐
│  SafeArea                           │
│  ┌─────────────────────────────┐   │
│  │  AppBar                     │   │
│  │  - 标题: "物品寿命"          │   │
│  │  - 右侧: + 添加按钮          │   │
│  └─────────────────────────────┘   │
│                                     │
│  SingleChildScrollView              │
│  ┌─────────────────────────────┐   │
│  │  StatsCard (统计卡片)        │   │
│  │  - 总物品数                  │   │
│  │  - 日均成本                  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  ExpiringSection (即将到期)  │   │
│  │  - 横向滚动列表              │   │
│  │  - 过期警告卡片              │   │
│  └─────────────────────────────┘   │
│                                     │
│  SectionTitle: "全部物品" + 筛选    │
│                                     │
│  ListView.separated                 │
│  ┌─────────────────────────────┐   │
│  │  ItemCard 1                 │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │  ItemCard 2                 │   │
│  └─────────────────────────────┘   │
│  ...                                │
│                                     │
└─────────────────────────────────────┘
```

**尺寸规范**:
- AppBar高度: 56
- StatsCard高度: 120
- ExpiringSection高度: 140
- ItemCard高度: 自适应(最小88)
- 卡片间距: 12
- 页面边距: 16

**交互**:
- 下拉刷新: RefreshIndicator
- 左滑删除: FlutterSlidable
- 点击跳转: Navigator.push(ItemDetailScreen)

---

### 2.2 添加物品页 (AddItemScreen)

**布局结构**:
```
┌─────────────────────────────────────┐
│  SafeArea                           │
│  ┌─────────────────────────────┐   │
│  │  AppBar                     │   │
│  │  - 返回按钮                  │   │
│  │  - 标题: "添加物品"          │   │
│  └─────────────────────────────┘   │
│                                     │
│  SingleChildScrollView              │
│  padding: 16                        │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  ImagePicker                │   │
│  │  - 尺寸: 120x120            │   │
│  │  - 圆角: 12                 │   │
│  │  - 占位图标: Camera         │   │
│  └─────────────────────────────┘   │
│                                     │
│  Text: "物品名称 *"                 │
│  InputField                         │
│  - hint: "例如: iPhone 15"          │
│  - 必填验证                        │
│                                     │
│  Text: "分类"                       │
│  HorizontalListView                 │
│  - CategoryChip列表                │
│  - 高度: 40                         │
│  - 间距: 8                          │
│                                     │
│  Text: "购买日期 *"                 │
│  DatePickerField                    │
│  - 点击弹出日期选择器              │
│  - 默认: 今天                       │
│                                     │
│  Text: "购买价格"                   │
│  PriceInputField                    │
│  - 前缀: "¥"                        │
│  - 键盘: number                     │
│                                     │
│  Text: "预期寿命 *"                 │
│  DropdownField                      │
│  - 选项: 6/12/24/36/48/60月        │
│  - 默认: 24                         │
│                                     │
│  Text: "备注（可选）"               │
│  TextArea                           │
│  - maxLines: 3                      │
│  - hint: "添加备注..."              │
│                                     │
│  SizedBox(height: 32)               │
│                                     │
│  PrimaryButton                      │
│  - 文字: "保存"                     │
│  - 高度: 48                         │
│  - 全宽                            │
│                                     │
└─────────────────────────────────────┘
```

**表单验证**:
- 名称: 必填, 1-50字符
- 分类: 必填
- 购买日期: 必填, 不能是未来日期
- 价格: 可选, 必须>0
- 预期寿命: 必填, 1-120月

---

### 2.3 物品详情页 (ItemDetailScreen)

**布局结构**:
```
┌─────────────────────────────────────┐
│  SafeArea                           │
│  ┌─────────────────────────────┐   │
│  │  AppBar                     │   │
│  │  - 返回按钮                  │   │
│  │  - 标题: 物品名称            │   │
│  │  - 编辑按钮                  │   │
│  └─────────────────────────────┘   │
│                                     │
│  SingleChildScrollView              │
│  padding: 16                        │
│                                     │
│  Center(                            │
│    Container(                       │
│      width: 160,                    │
│      height: 160,                   │
│      decoration: BoxDecoration(     │
│        borderRadius: 12,            │
│        image: DecorationImage(...), │
│      ),                             │
│      child: 分类图标占位,           │
│    ),                               │
│  ),                                 │
│                                     │
│  Center(                            │
│    Column(                          │
│      children: [                    │
│      Text(物品名称, style: title),  │
│      SizedBox(height: 4),           │
│      Chip(分类标签),                │
│    ],                               │
│  ),                                 │
│                                     │
│  SizedBox(height: 24),              │
│                                     │
│  // 寿命进度圆环                    │
│  Center(                            │
│    LifespanCircle(                  │
│      size: 200,                     │
│      progress: 0.8,                 │
│      remainingMonths: 24,           │
│      totalMonths: 36,               │
│      color: 根据状态变色,           │
│    ),                               │
│  ),                                 │
│                                     │
│  SizedBox(height: 24),              │
│                                     │
│  // 成本分析卡片                    │
│  Card(                              │
│    child: Padding(                  │
│      padding: 16,                   │
│      child: Column(                 │
│        children: [                  │
│          Row(                       │
│            Text('购买价格'),        │
│            Text('¥8,999'),          │
│          ),                         │
│          Divider(),                 │
│          Row(...日均成本...),       │
│          Row(...已用天数...),       │
│          Row(...预计总成本...),     │
│        ],                           │
│      ),                             │
│    ),                               │
│  ),                                 │
│                                     │
│  SizedBox(height: 24),              │
│                                     │
│  // 详细信息                        │
│  InfoRow(label: '购买日期', value: '2024-01-15'),  │
│  InfoRow(label: '添加时间', value: '2024-03-24'),  │
│                                     │
│  SizedBox(height: 8),               │
│                                     │
│  Text('备注'),                      │
│  Text(备注内容, style: caption),    │
│                                     │
│  SizedBox(height: 32),              │
│                                     │
│  // 删除按钮                        │
│  OutlinedButton(                    │
│    onPressed: _confirmDelete,       │
│    style: OutlinedButton.styleFrom( │
│      foregroundColor: Colors.red,   │
│    ),                               │
│    child: Text('删除物品'),         │
│  ),                                 │
│                                     │
└─────────────────────────────────────┘
```

---

### 2.4 统计页 (StatsScreen)

**布局结构**:
```
┌─────────────────────────────────────┐
│  SafeArea                           │
│  ┌─────────────────────────────┐   │
│  │  AppBar: "统计洞察"          │   │
│  └─────────────────────────────┘   │
│                                     │
│  SingleChildScrollView              │
│  padding: 16                        │
│                                     │
│  // 概览卡片                        │
│  Card(                              │
│    child: Padding(16),              │
│      Row(                           │
│        Expanded(总物品),            │
│        Expanded(总花费),            │
│        Expanded(日均成本),          │
│      ),                             │
│    ),                               │
│  ),                                 │
│                                     │
│  SizedBox(height: 24),              │
│                                     │
│  SectionTitle('分类占比'),          │
│                                     │
│  Card(                              │
│    height: 200,                     │
│    child: PieChart(...),            │
│  ),                                 │
│                                     │
│  SizedBox(height: 24),              │
│                                     │
│  SectionTitle('消费趋势'),          │
│                                     │
│  Card(                              │
│    height: 200,                     │
│    child: LineChart(...),           │
│  ),                                 │
│                                     │
│  SizedBox(height: 24),              │
│                                     │
│  SectionTitle('即将到期', trailing: '查看全部>'),  │
│                                     │
│  // 即将到期物品列表                │
│  ListView.builder(                  │
│    shrinkWrap: true,                │
│    physics: NeverScrollableScrollPhysics(),  │
│    itemBuilder: (context, index) =>    │
│      ItemCard(compact: true),       │
│  ),                                 │
│                                     │
└─────────────────────────────────────┘
```

---

### 2.5 设置页 (SettingsScreen)

**布局结构**:
```
┌─────────────────────────────────────┐
│  SafeArea                           │
│  ┌─────────────────────────────┐   │
│  │  AppBar: "设置"              │   │
│  └─────────────────────────────┘   │
│                                     │
│  ListView(                          │
│    // 数据管理                      │
│    SectionHeader('数据管理'),       │
│    SwitchListTile(                  │
│      title: '云同步',               │
│      subtitle: '备份到Firebase',    │
│      value: isCloudSyncEnabled,     │
│    ),                               │
│    ListTile(                        │
│      title: '导出数据',             │
│      trailing: Icon(Icons.chevron_right),  │
│      onTap: _exportData,            │
│    ),                               │
│    ListTile(                        │
│      title: '导入数据',             │
│      trailing: Icon(Icons.chevron_right),  │
│    ),                               │
│    ListTile(                        │
│      title: '清空数据',             │
│      textColor: Colors.red,         │
│      onTap: _confirmClearData,      │
│    ),                               │
│                                     │
│    Divider(),                       │
│                                     │
│    // 提醒设置                      │
│    SectionHeader('提醒设置'),       │
│    SwitchListTile(                  │
│      title: '寿命提醒',             │
│      value: isReminderEnabled,      │
│    ),                               │
│    ListTile(                        │
│      title: '提前提醒',             │
│      trailing: Text('7天 >'),       │
│      onTap: _selectReminderDays,    │
│    ),                               │
│                                     │
│    Divider(),                       │
│                                     │
│    // 外观                          │
│    SectionHeader('外观'),           │
│    SwitchListTile(                  │
│      title: '深色模式',             │
│      value: isDarkMode,             │
│    ),                               │
│                                     │
│    Divider(),                       │
│                                     │
│    // 关于                          │
│    SectionHeader('关于'),           │
│    ListTile(                        │
│      title: '版本',                 │
│      trailing: Text('1.0.0'),       │
│    ),                               │
│    ListTile(                        │
│      title: '反馈建议',             │
│      trailing: Icon(Icons.chevron_right),  │
│    ),                               │
│    ListTile(                        │
│      title: '隐私政策',             │
│      trailing: Icon(Icons.chevron_right),  │
│    ),                               │
│  ),                                 │
│                                     │
└─────────────────────────────────────┘
```

---

## 3. 组件规范

### 3.1 物品卡片 (ItemCard)

```dart
class ItemCard extends StatelessWidget {
  final Item item;
  final VoidCallback? onTap;
  final VoidCallback? onDelete;
  final bool compact; // 紧凑模式（用于统计页）
  
  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadius.large),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.large),
        child: Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 第一行: 图标 + 名称 + 箭头
              Row(
                children: [
                  _buildCategoryIcon(),
                  SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Text(
                      item.name,
                      style: AppTypography.title,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  Icon(Icons.chevron_right, color: AppColors.textTertiary),
                ],
              ),
              SizedBox(height: AppSpacing.xs),
              // 第二行: 分类
              Text(
                item.category,
                style: AppTypography.caption,
              ),
              SizedBox(height: AppSpacing.md),
              // 第三行: 寿命条
              LifespanBar(
                progress: item.progressPercent / 100,
                color: _getStatusColor(item),
              ),
              SizedBox(height: AppSpacing.sm),
              // 第四行: 剩余时间 + 日均成本
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    item.isExpired 
                      ? '已过期' 
                      : '剩余${item.remainingMonths}个月',
                    style: AppTypography.caption,
                  ),
                  Text(
                    '¥${item.dailyCost.toStringAsFixed(1)}/天',
                    style: AppTypography.caption.copyWith(
                      color: AppColors.primary,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 3.2 寿命条 (LifespanBar)

```dart
class LifespanBar extends StatelessWidget {
  final double progress; // 0.0 - 1.0
  final Color color;
  final double height;
  
  const LifespanBar({
    required this.progress,
    required this.color,
    this.height = 6,
  });
  
  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(height / 2),
      child: Container(
        height: height,
        decoration: BoxDecoration(
          color: AppColors.divider,
          borderRadius: BorderRadius.circular(height / 2),
        ),
        child: FractionallySizedBox(
          alignment: Alignment.centerLeft,
          widthFactor: progress.clamp(0.0, 1.0),
          child: Container(
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(height / 2),
            ),
          ),
        ),
      ),
    );
  }
}
```

### 3.3 主按钮 (PrimaryButton)

```dart
class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 48,
      width: double.infinity,
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.medium),
          ),
          elevation: 0,
        ),
        child: isLoading
          ? SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: Colors.white,
              ),
            )
          : Text(
              text,
              style: AppTypography.body.copyWith(
                color: Colors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
      ),
    );
  }
}
```

### 3.4 输入框 (InputField)

```dart
class InputField extends StatelessWidget {
  final String label;
  final String? hint;
  final TextEditingController? controller;
  final FormFieldValidator<String>? validator;
  final TextInputType? keyboardType;
  final Widget? prefix;
  final int? maxLines;
  final bool required;
  
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          required ? '$label *' : label,
          style: AppTypography.caption,
        ),
        SizedBox(height: AppSpacing.xs),
        TextFormField(
          controller: controller,
          validator: validator,
          keyboardType: keyboardType,
          maxLines: maxLines ?? 1,
          decoration: InputDecoration(
            hintText: hint,
            prefixIcon: prefix,
            contentPadding: EdgeInsets.symmetric(
              horizontal: AppSpacing.md,
              vertical: AppSpacing.md,
            ),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(AppRadius.medium),
              borderSide: BorderSide(color: AppColors.divider),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(AppRadius.medium),
              borderSide: BorderSide(color: AppColors.divider),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(AppRadius.medium),
              borderSide: BorderSide(color: AppColors.primary),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(AppRadius.medium),
              borderSide: BorderSide(color: AppColors.expired),
            ),
          ),
        ),
      ],
    );
  }
}
```

---

## 4. 交付清单

### 4.1 已完成 ✅
- [x] 设计系统（色彩/字体/间距/圆角）
- [x] 页面布局详细规范（5个页面）
- [x] 组件规范（ItemCard/LifespanBar/PrimaryButton/InputField）
- [x] 交互说明

### 4.2 待后续优化（有UI设计工具后）
- [ ] Figma设计稿
- [ ] 高保真视觉稿
- [ ] 切图资源包

---

## 5. 给开发的说明

**本设计规范可直接用于开发**，包含：
- 完整的布局结构
- 精确的尺寸数值
- 颜色代码（可直接复制到Dart）
- 组件伪代码（可直接实现）

**开发顺序建议**:
1. 先搭建设计系统（colors.dart/typography.dart）
2. 实现基础组件（ItemCard/InputField/Button）
3. 逐个页面实现（Home → Add → Detail → Stats → Settings）

---

*UI/UX Designer*  
*INSIGHT AI STUDIO*  
*2026-03-24*
