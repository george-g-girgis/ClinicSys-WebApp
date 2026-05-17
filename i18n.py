"""
i18n.py — Internationalisation support for ClinicSys.

Provides English and Arabic translations with a simple t(key) lookup.
"""

_current_lang = "en"

TRANSLATIONS = {
    "en": {
        # ── Login ────────────────────────────────────────────────────
        "app_title":        "ClinicSys — Clinic Management System",
        "login_title":      "ClinicSys — Login",
        "brand":            "🏥  ClinicSys",
        "sign_in":          "Sign in to continue",
        "username":         "Username",
        "password":         "Password",
        "enter_username":   "Enter username",
        "enter_password":   "Enter password",
        "login":            "Login",
        "fill_both":        "Please fill in both fields.",
        "invalid_creds":    "Invalid username or password.",

        # ── Dashboard ───────────────────────────────────────────────
        "dashboard_sub":    "Management Dashboard",
        "patients":         "Patients",
        "doctors":          "Doctors",
        "inventory":        "Inventory",
        "billing":          "Billing",
        "logout":           "Logout",
        "exit":             "Exit",
        "settings":         "Settings",
        "theme":            "Theme",
        "language":         "Language",
        "dark":             "Dark",
        "light":            "Light",

        # ── Patients ────────────────────────────────────────────────
        "patient_title":    "👥  Patients",
        "add_patient":      "＋  Add Patient",
        "export_csv":       "📤  Export CSV",
        "search_patients":  "🔍  Search patients by name…",
        "search_patients_hint": "Type a patient name to filter results",
        "patient_details":  "Patient Details",
        "full_name":        "Full Name",
        "age":              "Age",
        "phone":            "Phone",
        "medical_history":  "Medical History",
        "allergies":        "Allergies",
        "next_appointment": "Next Appointment",
        "name_required":    "Full Name is required.",

        # ── Doctors ─────────────────────────────────────────────────
        "doctor_title":     "🩺  Doctors",
        "add_doctor":       "＋  Add Doctor",
        "search_doctors":   "🔍  Search doctors by name…",
        "search_doctors_hint": "Type a doctor name to filter results",
        "doctor_details":   "Doctor Details",
        "name":             "Name",
        "specialty":        "Specialty",
        "dr_name_required": "Name is required.",

        # ── Inventory ──────────────────────────────────────────────
        "inventory_title":  "📦  Inventory",
        "add_item":         "＋  Add Item",
        "search_inventory": "🔍  Search inventory by item name…",
        "search_inventory_hint": "Type an item name to filter results",
        "item_details":     "Item Details",
        "item_name":        "Item Name",
        "quantity":         "Quantity",
        "expiry_date":      "Expiry Date",
        "item_required":    "Item Name is required.",
        "qty_required":     "Quantity must be a whole number.",

        # ── Billing ────────────────────────────────────────────────
        "billing_title":    "💵  Billing",
        "add_bill":         "＋  Add Bill",
        "search_billing":   "🔍  Search bills by patient name…",
        "search_billing_hint": "Type a patient name to filter billing records",
        "bill_details":     "Bill Details",
        "patient":          "Patient",
        "amount":           "Amount",
        "date":             "Date",
        "status":           "Status",
        "select_patient":   "Please select a valid patient.",
        "amount_invalid":   "Amount must be a number.",
        "date_required":    "Date is required.",

        # ── Common ─────────────────────────────────────────────────
        "save":             "Save",
        "update":           "Update",
        "cancel":           "Cancel",
        "confirm":          "Confirm",
        "validation":       "Validation",
        "export":           "Export",
        "edit_ctx":         "✏️  Edit",
        "delete_ctx":       "🗑️  Delete",
        "exported_msg":     "Exported {count} records to:\n{path}",
        "delete_patient":   "Delete patient #{id}?",
        "delete_doctor":    "Delete doctor #{id}?",
        "delete_item":      "Delete item #{id}?",
        "delete_bill":      "Delete bill #{id}?",
        "phone_val_err":    "Phone number must be exactly 11 digits.",
        "birth_date":       "Birth Date",
        "other":            "Other...",
        "status_change":    "Status Change",
        "save_status":      "Save Status",

        # ── Users ──────────────────────────────────────────────────
        "users":            "Users",
        "users_title":      "👤  User Management",
        "add_user":         "＋  Add User",
        "search_users":     "🔍  Search users by username…",
        "search_users_hint": "Type a username to filter results",
        "user_details":     "User Details",
        "role":             "Role",
        "username_required": "Username is required.",
        "password_required": "Password is required for new users.",
        "username_exists":  "That username already exists.",
        "pw_blank_hint":    "Leave blank to keep current password",
        "delete_user":      "Delete user #{id}?",
        "cannot_delete_last": "Cannot delete the last admin user.",

        # ── Web App Additions ──────────────────────────────────────
        "search_btn":       "Search",
        "id":               "ID",
        "actions":          "Actions",
        "edit":             "Edit",
        "delete":           "Delete",
        "save_changes":     "Save Changes",
        
        "patients_db":      "👥 Patients Database",
        "no_patients":      "No patients found in database.",
        "new_patient_reg":  "New Patient Registration",
        "register_patient": "Register Patient",
        "update_patient_record": "Update Patient Record",

        "doctors_directory": "🩺 Doctors Directory",
        "doctor_name":      "Doctor Name",
        "unspecified":      "Unspecified",
        "no_doctors":       "No doctors found in directory.",
        "new_doctor_profile": "New Doctor Profile",
        "save_doctor":      "Save Doctor",
        "update_doctor_profile": "Update Doctor Profile",

        "inventory_hub":    "📦 Inventory Hub",
        "no_items":         "No items in inventory.",
        "new_inventory_item": "New Inventory Item",
        "update_item":      "Update Item",

        "billing_payments": "💵 Billing & Payments",
        "patient_name":     "Patient Name",
        "amount_usd":       "Amount ($)",
        "no_bills":         "No billing records found.",
        "create_new_bill":  "Create New Bill",
        "select_pt":        "-- Select Patient --",
        "create_bill":      "Create Bill",
        "update_bill_status": "Update Bill Status",
        "status_pending":   "Pending",
        "status_paid":      "Paid",

        "user_management":  "👤 User Management",
        "security_note_strong": "Security Note:",
        "security_note_text": "Passwords are hashed using bcrypt. When editing an existing user, leave the password field blank to keep their current password.",
        "system_role":      "System Role",
        "no_users":         "No users found.",
        "create_new_user":  "Create New User",
        "create_user":      "Create User",
        "update_user_roles": "Update User Roles",
        "admin":            "Admin",
        "staff":            "Staff",
    },

    "ar": {
        # ── Login ────────────────────────────────────────────────────
        "app_title":        "ClinicSys — نظام إدارة العيادة",
        "login_title":      "ClinicSys — تسجيل الدخول",
        "brand":            "🏥  ClinicSys",
        "sign_in":          "سجّل الدخول للمتابعة",
        "username":         "اسم المستخدم",
        "password":         "كلمة المرور",
        "enter_username":   "أدخل اسم المستخدم",
        "enter_password":   "أدخل كلمة المرور",
        "login":            "دخول",
        "fill_both":        "يرجى ملء جميع الحقول.",
        "invalid_creds":    "اسم المستخدم أو كلمة المرور غير صحيحة.",

        # ── Dashboard ───────────────────────────────────────────────
        "dashboard_sub":    "لوحة الإدارة",
        "patients":         "المرضى",
        "doctors":          "الأطباء",
        "inventory":        "المخزون",
        "billing":          "الفواتير",
        "logout":           "تسجيل الخروج",
        "exit":             "خروج",
        "settings":         "الإعدادات",
        "theme":            "المظهر",
        "language":         "اللغة",
        "dark":             "داكن",
        "light":            "فاتح",

        # ── Patients ────────────────────────────────────────────────
        "patient_title":    "👥  المرضى",
        "add_patient":      "＋  إضافة مريض",
        "export_csv":       "📤  تصدير CSV",
        "search_patients":  "🔍  ابحث عن مريض بالاسم…",
        "search_patients_hint": "اكتب اسم المريض لتصفية النتائج",
        "patient_details":  "بيانات المريض",
        "full_name":        "الاسم الكامل",
        "age":              "العمر",
        "phone":            "الهاتف",
        "medical_history":  "التاريخ الطبي",
        "allergies":        "الحساسية",
        "next_appointment": "الموعد القادم",
        "name_required":    "الاسم الكامل مطلوب.",

        # ── Doctors ─────────────────────────────────────────────────
        "doctor_title":     "🩺  الأطباء",
        "add_doctor":       "＋  إضافة طبيب",
        "search_doctors":   "🔍  ابحث عن طبيب بالاسم…",
        "search_doctors_hint": "اكتب اسم الطبيب لتصفية النتائج",
        "doctor_details":   "بيانات الطبيب",
        "name":             "الاسم",
        "specialty":        "التخصص",
        "dr_name_required": "الاسم مطلوب.",

        # ── Inventory ──────────────────────────────────────────────
        "inventory_title":  "📦  المخزون",
        "add_item":         "＋  إضافة صنف",
        "search_inventory": "🔍  ابحث عن صنف بالاسم…",
        "search_inventory_hint": "اكتب اسم الصنف لتصفية النتائج",
        "item_details":     "بيانات الصنف",
        "item_name":        "اسم الصنف",
        "quantity":         "الكمية",
        "expiry_date":      "تاريخ الانتهاء",
        "item_required":    "اسم الصنف مطلوب.",
        "qty_required":     "الكمية يجب أن تكون رقمًا صحيحًا.",

        # ── Billing ────────────────────────────────────────────────
        "billing_title":    "💵  الفواتير",
        "add_bill":         "＋  إضافة فاتورة",
        "search_billing":   "🔍  ابحث عن فاتورة باسم المريض…",
        "search_billing_hint": "اكتب اسم المريض لتصفية سجلات الفواتير",
        "bill_details":     "بيانات الفاتورة",
        "patient":          "المريض",
        "amount":           "المبلغ",
        "date":             "التاريخ",
        "status":           "الحالة",
        "select_patient":   "يرجى اختيار مريض صالح.",
        "amount_invalid":   "المبلغ يجب أن يكون رقمًا.",
        "date_required":    "التاريخ مطلوب.",

        # ── Common ─────────────────────────────────────────────────
        "save":             "حفظ",
        "update":           "تحديث",
        "cancel":           "إلغاء",
        "confirm":          "تأكيد",
        "validation":       "تحقق",
        "export":           "تصدير",
        "edit_ctx":         "✏️  تعديل",
        "delete_ctx":       "🗑️  حذف",
        "exported_msg":     "تم تصدير {count} من السجلات إلى:\n{path}",
        "delete_patient":   "إزالة المريض رقم {id}؟",
        "delete_doctor":    "إزالة الطبيب رقم {id}؟",
        "delete_item":      "حذف الصنف رقم {id}؟",
        "delete_bill":      "حذف الفاتورة رقم {id}؟",
        "phone_val_err":    "يجب أن يتكون رقم الهاتف من 11 رقماً بالضبط.",
        "birth_date":       "تاريخ الميلاد",
        "other":            "أخرى...",
        "status_change":    "تغيير الحالة",
        "save_status":      "حفظ الحالة",

        # ── Users ──────────────────────────────────────────────────
        "users":            "المستخدمون",
        "users_title":      "👤  إدارة المستخدمين",
        "add_user":         "＋  إضافة مستخدم",
        "search_users":     "🔍  ابحث عن مستخدم…",
        "search_users_hint": "اكتب اسم المستخدم لتصفية النتائج",
        "user_details":     "بيانات المستخدم",
        "role":             "الدور",
        "username_required": "اسم المستخدم مطلوب.",
        "password_required": "كلمة المرور مطلوبة للمستخدمين الجدد.",
        "username_exists":  "اسم المستخدم موجود بالفعل.",
        "pw_blank_hint":    "اتركه فارغًا للاحتفاظ بكلمة المرور الحالية",
        "delete_user":      "حذف المستخدم رقم {id}؟",
        "cannot_delete_last": "لا يمكن حذف آخر مستخدم مسؤول.",

        # ── Web App Additions ──────────────────────────────────────
        "search_btn":       "بحث",
        "id":               "المُعرف",
        "actions":          "إجراءات",
        "edit":             "تعديل",
        "delete":           "حذف",
        "save_changes":     "حفظ التغييرات",
        
        "patients_db":      "👥 قاعدة بيانات المرضى",
        "no_patients":      "لا يوجد مرضى في قاعدة البيانات.",
        "new_patient_reg":  "تسجيل مريض جديد",
        "register_patient": "تسجيل مريض",
        "update_patient_record": "تحديث سجل المريض",

        "doctors_directory": "🩺 دليل الأطباء",
        "doctor_name":      "اسم الطبيب",
        "unspecified":      "غير محدد",
        "no_doctors":       "لا يوجد أطباء في الدليل.",
        "new_doctor_profile": "ملف طبيب جديد",
        "save_doctor":      "حفظ الطبيب",
        "update_doctor_profile": "تحديث ملف الطبيب",

        "inventory_hub":    "📦 مركز المخزون",
        "no_items":         "لا توجد عناصر في المخزون.",
        "new_inventory_item": "عنصر مخزون جديد",
        "update_item":      "تحديث العنصر",

        "billing_payments": "💵 الفواتير والمدفوعات",
        "patient_name":     "اسم المريض",
        "amount_usd":       "المبلغ ($)",
        "no_bills":         "لم يتم العثور على سجلات فواتير.",
        "create_new_bill":  "إنشاء فاتورة جديدة",
        "select_pt":        "-- اختر المريض --",
        "create_bill":      "إنشاء الفاتورة",
        "update_bill_status": "تحديث حالة الفاتورة",
        "status_pending":   "قيد الانتظار",
        "status_paid":      "مدفوع",

        "user_management":  "👤 إدارة المستخدمين",
        "security_note_strong": "ملاحظة أمنية:",
        "security_note_text": "كلمات المرور مشفرة. عند تعديل مستخدم موجود، اترك حقل كلمة المرور فارغاً للاحتفاظ بكلمة المرور الحالية.",
        "system_role":      "دور النظام",
        "no_users":         "لم يتم العثور على مستخدمين.",
        "create_new_user":  "إنشاء مستخدم جديد",
        "create_user":      "إنشاء مستخدم",
        "update_user_roles": "تحديث أدوار المستخدم",
        "admin":            "مسؤول",
        "staff":            "موظف",
    },
}


def get_lang() -> str:
    """Return the current language code ('en' or 'ar')."""
    return _current_lang


def set_lang(lang: str):
    """Set the current language ('en' or 'ar')."""
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang


def t(key: str) -> str:
    """Translate *key* using the current language. Falls back to English."""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["en"]).get(
        key, TRANSLATIONS["en"].get(key, key)
    )


def font_family() -> str:
    """Return the best font family for the current language.

    Tahoma has excellent Arabic glyph rendering on Windows.
    Segoe UI is the modern Windows default for Latin text.
    """
    return "Tahoma" if _current_lang == "ar" else "Segoe UI"


def font_size(base: int) -> int:
    """Return an adjusted font size — Arabic text is bumped up slightly."""
    if _current_lang == "ar":
        return base + 1
    return base


def is_rtl() -> bool:
    """Return True if the current language is right-to-left."""
    return _current_lang == "ar"

