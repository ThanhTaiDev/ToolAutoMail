# Hướng Dẫn Phát Hành ToolAutoMail

## 1. Build File .exe

Chạy script build:

```cmd
build_exe.bat
```

File .exe sẽ được tạo tại: `dist\ToolAutoMail.exe`

## 2. Tạo GitHub Release

### Bước 1: Vào GitHub Repository
- Truy cập: https://github.com/ThanhTaiDev/ToolAutoMail
- Click vào tab **Releases** (bên phải)

### Bước 2: Create New Release
- Click nút **"Draft a new release"**

### Bước 3: Điền thông tin Release

**Tag version**: (ví dụ: `v1.2.0`)
```
v1.2.0
```

**Release title**: (ví dụ)
```
ToolAutoMail v1.2.0 - Standalone Executable
```

**Description**: (ví dụ)
```markdown
## 🎉 Phiên bản .exe độc lập

Từ phiên bản này, ToolAutoMail được đóng gói thành file .exe, 
người dùng không cần cài Python nữa!

### 📥 Cài đặt nhanh

**Cách 1: Tự động (khuyến nghị)**
```powershell
irm https://raw.githubusercontent.com/ThanhTaiDev/ToolAutoMail/main/scripts/install.ps1 | iex
```

**Cách 2: Thủ công**
1. Tải file `ToolAutoMail.exe` ở dưới
2. Chạy trực tiếp

### ⚠️ Windows Defender Warning
Nếu Windows Defender báo cảnh báo, đây là false positive do file .exe 
chưa có chữ ký số. Bạn có thể bỏ qua bằng cách click "More info" → "Run anyway".

### 📝 Changelog
- ✅ Đóng gói thành .exe standalone
- ✅ Không cần cài Python
- ✅ Dễ dàng phát hành và cài đặt
```

### Bước 4: Upload file .exe
- Kéo thả file `dist\ToolAutoMail.exe` vào mục **"Attach binaries"**

### Bước 5: Publish
- Click **"Publish release"**

## 3. Lấy Link Download Trực Tiếp

Sau khi publish, link download sẽ có dạng:

```
https://github.com/ThanhTaiDev/ToolAutoMail/releases/download/v1.2.0/ToolAutoMail.exe
```

Format:
```
https://github.com/{username}/{repo}/releases/download/{tag}/{filename}
```

## 4. Cập Nhật Script Install (Tự động)

Script `install.ps1` đã được cập nhật để tải file .exe từ release mới nhất.

## 5. Test Trước Khi Phát Hành

✅ Test file .exe trên máy local  
✅ Test trên máy không có Python  
✅ Test trên máy sạch (fresh Windows)  
✅ Test script install.ps1 với link mới  

## Lưu Ý Bảo Mật

- ⚠️ File .exe vẫn có thể bị reverse engineer (nhưng khó hơn .py rất nhiều)
- ⚠️ Nếu muốn bảo mật hơn, cân nhắc thêm PyArmor hoặc các công cụ obfuscation khác
- ⚠️ Không nên lưu mật khẩu/token cứng trong source code
