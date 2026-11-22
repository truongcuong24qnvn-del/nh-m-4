import csv, json, re, tkinter as tk
from datetime import date
from tkinter import ttk, messagebox, filedialog, simpledialog
from config import APP_NAME, CURRENCIES, DATA_FILE
from storage import JsonStorage
from services import ParkingService

VI_TEXT={
    "QUAN LY BAI XE":"QUẢN LÝ BÃI ĐỖ XE","Tong quan":"Tổng quan","So do bai xe":"Sơ đồ bãi xe","Phuong tien":"Phương tiện","Luot gui xe":"Lượt gửi xe","Bao cao":"Báo cáo","Phan hoi khach hang":"Phản hồi khách hàng","Cai dat":"Cài đặt",
    "Quan tri vien":"Quản trị viên","Nhan vien":"Nhân viên","HE THONG HOAT DONG":"HỆ THỐNG ĐANG HOẠT ĐỘNG","Dang nhap":"Đăng nhập","Dang xuat":"Đăng xuất","Doi mat khau":"Đổi mật khẩu",
    "TONG QUAN":"TỔNG QUAN","Xin chao, ":"Xin chào, ","Day la tinh hinh bai xe cua ban hom nay.":"Đây là tình hình bãi xe hôm nay.","TONG SO VI TRI":"TỔNG SỐ VỊ TRÍ","XE DANG GUI":"XE ĐANG GỬI","DOANH THU THANG":"DOANH THU THÁNG","LUOT XE HOM NAY":"LƯỢT XE HÔM NAY","Cap nhat truc tiep":"Cập nhật trực tiếp","Vi tri · cap nhat truc tiep":"Vị trí · cập nhật trực tiếp","Muc do su dung":"Mức độ sử dụng","Ty le lap day hien tai":"Tỷ lệ lấp đầy hiện tại","Dang su dung":"Đang sử dụng","Con trong":"Còn trống","Bao tri":"Bảo trì","Hoat dong gan day":"Hoạt động gần đây","Bien so":"Biển số","Loai xe":"Loại xe","O do":"Ô đỗ","Thoi gian vao":"Thời gian vào","Trang thai":"Trạng thái","Phi / thao tac":"Phí / thao tác",
    "Quan ly vi tri do":"Quản lý vị trí đỗ","Ma vi tri":"Mã vị trí","Them o":"Thêm ô","Bao tri / Mo lai":"Bảo trì / Mở lại","Xoa o trong":"Xóa ô trống","Xe dang do":"Xe đang đỗ","Danh sach phuong tien":"Danh sách phương tiện","Tim theo bien so, chu xe hoac dien thoai":"Tìm theo biển số, chủ xe hoặc điện thoại","Chu xe":"Chủ xe","Dien thoai":"Điện thoại","Tinh trang":"Tình trạng","Them xe":"Thêm xe","Cap nhat chon":"Cập nhật mục chọn","Xoa xe":"Xóa xe","Nhan xe va luot gui":"Nhận xe và lượt gửi","Bien so xe":"Biển số xe","Chu xe (khong bat buoc)":"Chủ xe (không bắt buộc)","Nhan xe vao":"Nhận xe vào","Tra xe dang chon":"Trả xe đang chọn","Tim bien so / ma o":"Tìm biển số / mã ô","Tat ca":"Tất cả","Dang gui":"Đang gửi","Da thanh toan":"Đã thanh toán","Tu ngay":"Từ ngày","Den ngay":"Đến ngày","Thong ke":"Thống kê","Lay ty gia API":"Lấy tỷ giá API","Xuat CSV":"Xuất CSV","Phan hoi khach hang":"Phản hồi khách hàng","Ghi nhan y kien, theo doi danh gia va gui phan hoi tu bai xe.":"Ghi nhận ý kiến, theo dõi đánh giá và phản hồi khách hàng.","Ghi nhan danh gia moi":"Ghi nhận đánh giá mới","Ten khach":"Tên khách hàng","Bien so (tuy chon)":"Biển số (không bắt buộc)","Nhom":"Nhóm góp ý","Sao":"Sao","Noi dung":"Nội dung","Luu phan hoi":"Lưu góp ý","Tim ten, bien so hoac noi dung":"Tìm tên, biển số hoặc nội dung","Tra loi chon":"Trả lời mục chọn","Xoa chon":"Xóa mục chọn","Ma":"Mã","Ngay gui":"Ngày gửi","Khach hang":"Khách hàng","Phan hoi bai xe":"Phản hồi của bãi xe","Chua phan hoi":"Chưa phản hồi","Cau hinh he thong":"Cấu hình hệ thống","Don gia gui xe":"Đơn giá gửi xe","Luu gia":"Lưu giá","Tao tai khoan":"Tạo tài khoản","Ten dang nhap":"Tên đăng nhập","Mat khau (6+ ky tu)":"Mật khẩu (từ 6 ký tự)","Ho ten":"Họ và tên","Vai tro":"Vai trò","Tai khoan va phan quyen":"Tài khoản và phân quyền","Mat khau moi (de trong neu khong doi)":"Mật khẩu mới (để trống nếu không đổi)","Cap nhat tai khoan chon":"Cập nhật tài khoản đã chọn","Xoa tai khoan chon":"Xóa tài khoản đã chọn","Tao 5 xe demo ngau nhien":"Tạo 5 xe mẫu ngẫu nhiên","Sao luu JSON":"Sao lưu JSON","Khoi phuc JSON":"Khôi phục JSON","Nguoi dung":"Người dùng","Ngoai bai":"Ngoài bãi",
    "Xe may":"Xe máy","O to":"Ô tô","staff":"Nhân viên","admin":"Quản trị viên","Nhan vien":"Nhân viên","Co so vat chat":"Cơ sở vật chất","An toan":"An toàn","Thanh toan":"Thanh toán","Khac":"Khác"
}

VEHICLE_CODE={"Xe máy":"Xe may","Ô tô":"O to"}
CATEGORY_CODE={"Nhân viên":"Nhan vien","Cơ sở vật chất":"Co so vat chat","An toàn":"An toan","Thanh toán":"Thanh toan","Khác":"Khac"}
def show_vehicle(value): return {"Xe may":"Xe máy","O to":"Ô tô"}.get(value,value)
def show_status(value): return {"free":"Còn trống","occupied":"Đang sử dụng","maintenance":"Bảo trì","active":"Đang gửi","closed":"Đã thanh toán"}.get(value,value)
VI_TEXT.update({
    "CHAO MUNG TRO LAI":"CHÀO MỪNG TRỞ LẠI","Dang nhap":"Đăng nhập","Nhap tai khoan de tiep tuc quan ly bai xe.":"Nhập tài khoản để tiếp tục quản lý bãi xe.","TEN DANG NHAP":"TÊN ĐĂNG NHẬP","MAT KHAU":"MẬT KHẨU","Dang nhap  →":"Đăng nhập  →","Tai khoan demo\nQuan tri vien: admin / 123456\nNhan vien: nhanvien / 123456":"TÀI KHOẢN DÙNG THỬ\nQuản trị viên: admin / 123456\nNhân viên: nhanvien / 123456","Tao tai khoan nhan vien":"Tạo tài khoản nhân viên",
    "TONG QUAN":"TỔNG QUAN","Day la tinh hinh bai xe cua ban hom nay.":"Đây là tình hình bãi xe hôm nay.","TONG SO VI TRI":"TỔNG SỐ VỊ TRÍ","XE DANG GUI":"XE ĐANG GỬI","DOANH THU THANG":"DOANH THU THÁNG","LUOT XE HOM NAY":"LƯỢT XE HÔM NAY","Cap nhat truc tiep":"Cập nhật trực tiếp","So do bai xe":"Sơ đồ bãi xe","Nhan xe":"Nhận xe","Vi tri · cap nhat truc tiep":"Vị trí · cập nhật trực tiếp","Muc do su dung":"Mức độ sử dụng","Ty le lap day hien tai":"Tỷ lệ lấp đầy hiện tại","Hoat dong gan day":"Hoạt động gần đây","Phi / thao tac":"Phí / thao tác","Thoi gian vao":"Thời gian vào","Xe dang do":"Xe đang đỗ","Tim theo bien so, chu xe hoac dien thoai":"Tìm theo biển số, chủ xe hoặc điện thoại","Chu xe":"Chủ xe","Dien thoai":"Điện thoại","Cap nhat chon":"Cập nhật mục đã chọn","Tinh trang":"Tình trạng","Nhan xe va luot gui":"Nhận xe và lượt gửi","Bien so xe":"Biển số xe","Chu xe (khong bat buoc)":"Chủ xe (không bắt buộc)","Nhan xe vao":"Nhận xe vào","Tra xe dang chon":"Trả xe đang chọn","Tim bien so / ma o":"Tìm biển số / mã ô","Tat ca":"Tất cả","Tu ngay":"Từ ngày","Den ngay":"Đến ngày","Thong ke":"Thống kê","Lay ty gia API":"Lấy tỷ giá API","Xuat CSV":"Xuất CSV",
    "Phan hoi khach hang":"Phản hồi khách hàng","Ghi nhan y kien, theo doi danh gia va gui phan hoi tu bai xe.":"Ghi nhận ý kiến, theo dõi đánh giá và phản hồi khách hàng.","Ghi nhan danh gia moi":"Ghi nhận đánh giá mới","Ten khach":"Tên khách hàng","Bien so (tuy chon)":"Biển số (không bắt buộc)","Nhom":"Nhóm góp ý","Noi dung":"Nội dung","Luu phan hoi":"Lưu góp ý","Tim ten, bien so hoac noi dung":"Tìm tên, biển số hoặc nội dung","Tra loi chon":"Trả lời mục đã chọn","Xoa chon":"Xóa mục đã chọn","Ngay gui":"Ngày gửi","Khach hang":"Khách hàng","Phan hoi bai xe":"Phản hồi của bãi xe","Chua phan hoi":"Chưa phản hồi","Cau hinh he thong":"Cấu hình hệ thống","Don gia gui xe":"Đơn giá gửi xe","Luu gia":"Lưu giá","Tao tai khoan":"Tạo tài khoản","Ten dang nhap":"Tên đăng nhập","Mat khau (6+ ky tu)":"Mật khẩu (từ 6 ký tự)","Ho ten":"Họ và tên","Vai tro":"Vai trò","Tai khoan va phan quyen":"Tài khoản và phân quyền","Mat khau moi (de trong neu khong doi)":"Mật khẩu mới (để trống nếu không đổi)","Cap nhat tai khoan chon":"Cập nhật tài khoản đã chọn","Xoa tai khoan chon":"Xóa tài khoản đã chọn","Tao 5 xe demo ngau nhien":"Tạo 5 xe mẫu ngẫu nhiên","Sao luu JSON":"Sao lưu JSON","Khoi phuc JSON":"Khôi phục JSON",
    "Con trong":"Còn trống","Dang su dung":"Đang sử dụng","Bao tri":"Bảo trì","Dang gui":"Đang gửi","Da thanh toan":"Đã thanh toán","Ngoai bai":"Ngoài bãi","Xe may":"Xe máy","O to":"Ô tô","staff":"Nhân viên","admin":"Quản trị viên","Nhan vien":"Nhân viên","Co so vat chat":"Cơ sở vật chất","An toan":"An toàn","Thanh toan":"Thanh toán","Khac":"Khác"
})
VI_TEXT.update({"ha quyen":"hạ quyền","giu lai":"giữ lại","dien thoai":"điện thoại","Khong sua":"Không sửa","tra xe truoc":"trả xe trước","da co":"đã có","bao toan":"bảo toàn","Bai":"Bãi","bai":"bãi","khong con":"không còn","hop le":"hợp lệ","khong phu hop":"không phù hợp","tu 1 den 5":"từ 1 đến 5","tu 8 den 600":"từ 8 đến 600","tu 3 den 600":"từ 3 đến 600","dung dinh dang":"đúng định dạng","truong du lieu bat buoc":"trường dữ liệu bắt buộc","khong khop voi":"không khớp với","do JSON":"đỗ JSON","da chot":"đã chốt","khong dong bo":"không đồng bộ","bi trung":"bị trùng","can co":"cần có","voi":"với","den":"đến"})
VI_TEXT.update({
    "PARKLY  ·  SMART PARKING MANAGEMENT":"PARKLY  ·  QUẢN LÝ BÃI ĐỖ THÔNG MINH","QUAN LY BAI XE":"QUẢN LÝ BÃI ĐỖ XE",
    "Quan ly vi tri do":"Quản lý vị trí đỗ","Ma vi tri":"Mã vị trí","Loai xe":"Loại xe","Them o":"Thêm ô","Bao tri / Mo lai":"Bảo trì / Mở lại","Xoa o trong":"Xóa ô trống","Ma o":"Mã ô","Trang thai":"Trạng thái","Xe dang do":"Xe đang đỗ",
    "Danh sach phuong tien":"Danh sách phương tiện","Bien so":"Biển số","Chu xe":"Chủ xe","Dien thoai":"Điện thoại","Tim theo bien so, chu xe hoac dien thoai":"Tìm theo biển số, chủ xe hoặc điện thoại","Them xe":"Thêm xe","Cap nhat chon":"Cập nhật mục đã chọn","Xoa xe":"Xóa xe","Tinh trang":"Tình trạng",
    "Nhan xe va luot gui":"Nhận xe và lượt gửi","Bien so xe":"Biển số xe","Chu xe (khong bat buoc)":"Chủ xe (không bắt buộc)","Nhan xe vao":"Nhận xe vào","Tra xe dang chon":"Trả xe đang chọn","Tim bien so / ma o":"Tìm biển số / mã ô","Tat ca":"Tất cả","Dang gui":"Đang gửi","Da thanh toan":"Đã thanh toán","Ma luot":"Mã lượt","Gio vao":"Giờ vào","Gio ra":"Giờ ra","Phi VND":"Phí (VND)",
    "Bao cao doanh thu":"Báo cáo doanh thu","Tu ngay":"Từ ngày","Den ngay":"Đến ngày","Thong ke":"Thống kê","Lay ty gia API":"Lấy tỷ giá API","Xuat CSV":"Xuất CSV","Vao":"Vào","Ra":"Ra",
    "Phan hoi khach hang":"Phản hồi khách hàng","Ghi nhan y kien, theo doi danh gia va gui phan hoi tu bai xe.":"Ghi nhận ý kiến, theo dõi đánh giá và phản hồi khách hàng.","Ghi nhan danh gia moi":"Ghi nhận đánh giá mới","Ten khach":"Tên khách hàng","Bien so (tuy chon)":"Biển số (không bắt buộc)","Nhom":"Nhóm góp ý","Sao":"Sao","Noi dung":"Nội dung","Luu phan hoi":"Lưu góp ý","Tim ten, bien so hoac noi dung":"Tìm tên, biển số hoặc nội dung","Tra loi chon":"Trả lời mục đã chọn","Xoa chon":"Xóa mục đã chọn","Ngay gui":"Ngày gửi","Khach hang":"Khách hàng","Phan hoi bai xe":"Phản hồi của bãi xe",
    "Cau hinh he thong":"Cấu hình hệ thống","Don gia gui xe":"Đơn giá gửi xe","Xe may VND/gio":"Xe máy (VND/giờ)","O to VND/gio":"Ô tô (VND/giờ)","Luu gia":"Lưu giá","Tao tai khoan":"Tạo tài khoản","Ten dang nhap":"Tên đăng nhập","Mat khau (6+ ky tu)":"Mật khẩu (từ 6 ký tự)","Ho ten":"Họ và tên","Vai tro":"Vai trò","Tai khoan va phan quyen":"Tài khoản và phân quyền","Mat khau moi (de trong neu khong doi)":"Mật khẩu mới (để trống nếu không đổi)","Cap nhat tai khoan chon":"Cập nhật tài khoản đã chọn","Xoa tai khoan chon":"Xóa tài khoản đã chọn","Tao 5 xe demo ngau nhien":"Tạo 5 xe mẫu ngẫu nhiên","Sao luu JSON":"Sao lưu JSON","Khoi phuc JSON":"Khôi phục JSON","Tep du lieu:":"Tệp dữ liệu:","Mat khau demo:":"Mật khẩu dùng thử:","nhanvien":"nhân viên",
    "Loi du lieu":"Lỗi dữ liệu","Sai ten dang nhap hoac mat khau":"Tên đăng nhập hoặc mật khẩu không đúng","Khong the tao tai khoan":"Không thể tạo tài khoản","Khong the doi mat khau":"Không thể đổi mật khẩu","Dang xuat":"Đăng xuất","Doi mat khau":"Đổi mật khẩu",
    "Loi API":"Lỗi API","Khong the tra loi":"Không thể trả lời","Khong the xoa":"Không thể xóa","Khong the them":"Không thể thêm","Khong the cap nhat":"Không thể cập nhật","Khong the nhan xe":"Không thể nhận xe","Khong the tra xe":"Không thể trả xe","Khong the khoi phuc":"Không thể khôi phục","Du lieu chua hop le":"Dữ liệu chưa hợp lệ","Xac nhan":"Xác nhận","Phan quyen":"Phân quyền","Chon xe":"Chọn xe","Chon vi tri":"Chọn vị trí","Chon o":"Chọn ô","Chon luot":"Chọn lượt","Chon phan hoi":"Chọn phản hồi","Chon tai khoan":"Chọn tài khoản",
    "khong hop le":"không hợp lệ","Khong tim thay":"Không tìm thấy","Khong the":"Không thể","khong the":"không thể","Nhap":"Nhập","Ten dang nhap":"Tên đăng nhập","Bien so":"Biển số","Dien thoai":"Điện thoại","vai tro":"vai trò","Mat khau":"Mật khẩu","mat khau":"mật khẩu","du lieu":"dữ liệu","Du lieu":"Dữ liệu","khong duoc":"không được","toi thieu":"tối thiểu","toi da":"tối đa","phai":"phải","can":"cần","vi tri":"vị trí","dang gui":"đang gửi","luot gui":"lượt gửi","xe may":"xe máy","o to":"ô tô","doanh thu":"doanh thu","bao cao":"báo cáo","khach hang":"khách hàng","phan hoi":"phản hồi","tai khoan":"tài khoản","xoa":"xóa","them":"thêm","sua":"sửa","dinh dang":"định dạng","khong hop le":"không hợp lệ","ngay":"ngày","ty gia":"tỷ giá","don gia":"đơn giá","duoc":"được","hay":"hãy","co the":"có thể"
})
VI_TEXT.update({
    "Ten dang nhap (3-24 ky tu):":"Tên đăng nhập (3–24 ký tự):","Ho va ten:":"Họ và tên:","Mat khau (toi thieu 6 ky tu):":"Mật khẩu (tối thiểu 6 ký tự):","Nhap mat khau hien tai:":"Nhập mật khẩu hiện tại:","Nhap mat khau moi (toi thieu 6 ky tu):":"Nhập mật khẩu mới (tối thiểu 6 ký tự):","Nhap noi dung phan hoi:":"Nhập nội dung phản hồi:",
    "Ban muon dang xuat khoi he thong?":"Bạn muốn đăng xuất khỏi hệ thống?","Da tao tai khoan nhan vien. Ban co the dang nhap.":"Đã tạo tài khoản nhân viên. Bạn có thể đăng nhập.","Da cap nhat mat khau":"Đã cập nhật mật khẩu","Hay chon danh gia can tra loi":"Hãy chọn đánh giá cần trả lời","Da luu loi tra loi":"Đã lưu lời trả lời","Hay chon danh gia can xoa":"Hãy chọn đánh giá cần xóa","Chi quan tri vien duoc xoa phan hoi":"Chỉ quản trị viên được xóa phản hồi","Da them phuong tien":"Đã thêm phương tiện","Chon dong can cap nhat":"Chọn dòng cần cập nhật","Chon dong can xoa":"Chọn dòng cần xóa","Da them o do":"Đã thêm ô đỗ","Hay chon o muon xoa":"Hãy chọn ô muốn xóa","Chon vi tri can cap nhat":"Chọn vị trí cần cập nhật","Chon luot gui dang mo":"Chọn lượt gửi đang mở","Da luu don gia":"Đã lưu đơn giá","Da tao tai khoan":"Đã tạo tài khoản","Hay chon tai khoan can cap nhat":"Hãy chọn tài khoản cần cập nhật","Da cap nhat vai tro/mat khau":"Đã cập nhật vai trò/mật khẩu","Hay chon tai khoan can xoa":"Hãy chọn tài khoản cần xóa","Da them 5 phuong tien ngau nhien":"Đã thêm 5 phương tiện ngẫu nhiên","Da luu ban sao JSON":"Đã lưu bản sao JSON","Du lieu hien tai se duoc sao luu truoc. Tiep tuc?":"Dữ liệu hiện tại sẽ được sao lưu trước. Tiếp tục?","Da nhap du lieu":"Đã nhập dữ liệu","Da them":"Đã thêm","Da cap nhat":"Đã cập nhật","Da luu":"Đã lưu","Da xuat":"Đã xuất","Da nhap":"Đã nhập","Tiep tuc?":"Tiếp tục?","Sai ten dang nhap hoac mat khau":"Tên đăng nhập hoặc mật khẩu không đúng",
    "Loi tep":"Lỗi tệp","Loi sao luu":"Lỗi sao lưu","Ty gia":"Tỷ giá","Xuat bao cao":"Xuất báo cáo","Sao luu":"Sao lưu","Khoi phuc":"Khôi phục","Cau hinh":"Cấu hình","Don gia khong hop le":"Đơn giá không hợp lệ","Nguon":"Nguồn","Cap nhat":"Cập nhật","Nhap":"Nhập","Tai khoan":"Tài khoản","Phuong tien":"Phương tiện","Vi tri":"Vị trí","Nhan xe":"Nhận xe","Thanh toan":"Thanh toán","Loi du lieu":"Lỗi dữ liệu","Chon dong":"Chọn dòng","duoc":"được","nguoi":"người","nhan vien":"nhân viên","phuong tien":"phương tiện","o do":"ô đỗ","so gio":"số giờ","phai":"phải","hien tai":"hiện tại","khong dung":"không đúng","da ton tai":"đã tồn tại","chua dung dinh dang":"chưa đúng định dạng","khong hop le":"không hợp lệ","it nhat":"ít nhất","toi thieu":"tối thiểu","ky tu":"ký tự","chi gom":"chỉ gồm","cham":"chấm","gach ngang":"gạch ngang","gach duoi":"gạch dưới","can giu lai":"cần giữ lại","mot tai khoan quan tri":"một tài khoản quản trị","dang dang nhap":"đang đăng nhập","xe dang gui":"xe đang gửi","tra xe truoc":"trả xe trước","bao toan lich su":"bảo toàn lịch sử","gom":"gồm","khong the xoa":"không thể xóa","lich su gui xe":"lịch sử gửi xe","bao cao":"báo cáo","khong ton tai":"không tồn tại","dang co xe":"đang có xe","xe da co":"xe đã có","luot gui dang mo":"lượt gửi đang mở","bai khong con":"bãi không còn","o trong phu hop":"ô trống phù hợp","luot dang gui":"lượt đang gửi","trang thai":"trạng thái","kiem tra":"kiểm tra","du lieu":"dữ liệu","truoc khi":"trước khi","thanh toan":"thanh toán","don gia":"đơn giá","khong duoc am":"không được âm","ngay bat dau":"ngày bắt đầu","truoc hoac bang":"trước hoặc bằng","ngay ket thuc":"ngày kết thúc","API khong tra":"API không trả","diem danh gia":"điểm đánh giá","noi dung":"nội dung","phan hoi":"phản hồi","thoi diem":"thời điểm","dinh dang":"định dạng"
})
VI_TEXT.update({
    "moi":"mới","Moi":"Mới","chu":"chữ","Chu":"Chữ","so":"số","So":"Số","hoac":"hoặc","Hoac":"Hoặc","du":"đủ","Du":"Đủ","hay":"hãy","Hay":"Hãy","de":"để","De":"Để","o":"ô","O":"Ô","phi":"phí","Phi":"Phí","diem":"điểm","Diem":"Điểm","danh gia":"đánh giá","Danh gia":"Đánh giá","bat dau":"bắt đầu","Bat dau":"Bắt đầu","Don gia":"Đơn giá","don gia":"đơn giá","Ngay":"Ngày","ngay":"ngày","Can":"Cần","can":"cần","Thieu":"Thiếu","thieu":"thiếu","Danh sach":"Danh sách","danh sach":"danh sách","Ho so":"Hồ sơ","ho so":"hồ sơ","Thoi diem":"Thời điểm","thoi diem":"thời điểm","Thong tin":"Thông tin","thong tin":"thông tin","cua":"của","Cua":"Của","bi":"bị","Bi":"Bị","khop":"khớp","dong bo":"đồng bộ","Dong bo":"Đồng bộ","luot da dong":"lượt đã đóng","Luot da dong":"Lượt đã đóng","vao":"vào","Vao":"Vào","lich su":"lịch sử","Lich su":"Lịch sử","ton tai":"tồn tại","Ton tai":"Tồn tại","gom":"gồm","Gom":"Gồm","tiep tuc":"tiếp tục","Tiep tuc":"Tiếp tục","ro rang":"rõ ràng","Rõ rang":"Rõ ràng","ket thuc":"kết thúc","Ket thuc":"Kết thúc","khach":"khách","Khach":"Khách","ten":"tên","Ten":"Tên","nhom":"nhóm","Nhom":"Nhóm","phan hoi":"phản hồi","Phan hoi":"Phản hồi","tra loi":"trả lời","Tra loi":"Trả lời","xoa":"xóa","Xoa":"Xóa","xuat":"xuất","Xuat":"Xuất","sao luu":"sao lưu","Sao luu":"Sao lưu","mau":"mẫu","Mau":"Mẫu","Nội dung":"Nội dung"
})

def translate_text(value):
    """Dịch nhãn và thông báo giao diện, giữ nguyên dữ liệu nghiệp vụ."""
    if not isinstance(value,str): return value
    if value in VI_TEXT: return VI_TEXT[value]
    for source,target in sorted(VI_TEXT.items(),key=lambda pair:len(pair[0]),reverse=True):
        if source:
            value=re.sub(r"(?<!\w)"+re.escape(source)+r"(?!\w)",lambda _match:target,value)
    return value

def _install_vietnamese_dialogs():
    """Giữ thông báo lỗi, xác nhận và hộp nhập liệu thống nhất tiếng Việt."""
    for name in ("showinfo","showwarning","showerror","askyesno"):
        original=getattr(messagebox,name)
        if getattr(original,"_parkly_vietnamese",False): continue
        def translated(title,message,*args,_original=original,**kwargs):
            return _original(translate_text(title),translate_text(message),*args,**kwargs)
        translated._parkly_vietnamese=True
        setattr(messagebox,name,translated)
    original=simpledialog.askstring
    if not getattr(original,"_parkly_vietnamese",False):
        def translated_input(title,prompt,*args,**kwargs):
            return original(translate_text(title),translate_text(prompt),*args,**kwargs)
        translated_input._parkly_vietnamese=True
        simpledialog.askstring=translated_input

_install_vietnamese_dialogs()

class StatusBadge(ttk.Label):
    """Tiện ích tùy chỉnh hiển thị trạng thái chỗ đỗ và lượt gửi."""
    COLORS={"free":"#138a67","occupied":"#bd7b17","maintenance":"#d84a57","active":"#bd7b17","closed":"#138a67"}
    TEXT={"free":"Còn trống","occupied":"Đang sử dụng","maintenance":"Bảo trì","active":"Đang gửi","closed":"Đã thanh toán"}
    def __init__(self,parent,status):
        super().__init__(parent,text=self.TEXT.get(status,status),foreground=self.COLORS.get(status,"#4568f5"),font=("Segoe UI",9,"bold"))

class ParkingApp:
    def __init__(self,root):
        self.root=root; root.title(APP_NAME)
        sw,sh=root.winfo_screenwidth(),root.winfo_screenheight()
        width=max(900,min(1440,sw-48)); height=max(620,min(940,sh-80))
        root.geometry(f"{width}x{height}"); root.minsize(min(1020,width),min(680,height))
        self.storage=JsonStorage(); self.service=ParkingService(self.storage); self.user=None
        self.style=ttk.Style(); self.style.theme_use("clam")
        self.style.configure(".",font=("Segoe UI",10))
        self.style.configure("TFrame",background="#f4f6fa")
        self.style.configure("Page.TFrame",background="#f4f6fa")
        self.style.configure("Panel.TFrame",background="#ffffff")
        self.style.configure("TLabel",font=("Segoe UI",10),background="#f4f6fa",foreground="#17243a")
        self.style.configure("Title.TLabel",font=("Segoe UI",22,"bold"),foreground="#17243a",background="#f4f6fa")
        self.style.configure("Treeview",rowheight=39,font=("Segoe UI",10),background="#ffffff",fieldbackground="#ffffff",foreground="#26344b")
        self.style.configure("Treeview.Heading",font=("Segoe UI",9,"bold"),background="#f7f9fc",foreground="#68758b",padding=10)
        self.style.map("Treeview",background=[("selected","#e8edff")],foreground=[("selected","#17243a")])
        self.style.configure("Accent.TButton",background="#4568f5",foreground="white",padding=9,font=("Segoe UI",10,"bold"))
        self.style.map("Accent.TButton",background=[("active","#3855e5")])
        self.style.configure("TButton",padding=(10,7),font=("Segoe UI",9))
        self.style.configure("TEntry",padding=7)
        self.style.configure("TCombobox",padding=6)
        self.style.configure("TLabelframe",background="#ffffff",bordercolor="#e6ebf2")
        self.style.configure("TLabelframe.Label",font=("Segoe UI",10,"bold"),foreground="#17243a")
        self.show_login()
    def clear(self):
        for w in self.root.winfo_children(): w.destroy()
    def show_login(self):
        self.clear(); self.root.configure(bg="#ffffff")
        sw,sh=self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        login_w=min(1050,sw-48); login_h=min(650,sh-80)
        self.root.geometry(f"{login_w}x{login_h}")
        shell=tk.Frame(self.root,bg="white"); shell.pack(fill="both",expand=True)
        left_width=int(login_w*.45)
        left=tk.Frame(shell,bg="#20366b",width=left_width); left.pack(side="left",fill="both"); left.pack_propagate(False)
        tk.Label(left,text="P   parkly",bg="#20366b",fg="white",font=("Segoe UI",20,"bold")).pack(anchor="nw",padx=46,pady=(48,0))
        tk.Label(left,text="Bãi xe vận hành\nnhẹ nhàng hơn.",bg="#20366b",fg="white",font=("Segoe UI",30,"bold"),justify="left").pack(anchor="w",padx=46,pady=(110,10))
        tk.Label(left,text="Từ một chỗ đỗ đến toàn bộ hoạt động.\nQuản lý trực quan, nhanh gọn mỗi ngày.",bg="#20366b",fg="#d5def2",font=("Segoe UI",11),justify="left").pack(anchor="w",padx=46)
        tk.Label(left,text="PARKLY  ·  QUẢN LÝ BÃI ĐỖ THÔNG MINH",bg="#20366b",fg="#b6c3e2",font=("Segoe UI",8,"bold")).pack(side="bottom",anchor="w",padx=46,pady=35)
        right=tk.Frame(shell,bg="white"); right.pack(side="left",fill="both",expand=True)
        box=tk.Frame(right,bg="white",padx=55); box.place(relx=.5,rely=.5,anchor="center")
        tk.Label(box,text="CHÀO MỪNG TRỞ LẠI",bg="white",fg="#4568f5",font=("Segoe UI",8,"bold")).pack(anchor="w")
        tk.Label(box,text="Đăng nhập",bg="white",fg="#17243a",font=("Segoe UI",24,"bold")).pack(anchor="w",pady=(5,3))
        tk.Label(box,text="Nhập tài khoản để tiếp tục quản lý bãi xe.",bg="white",fg="#7b879b",font=("Segoe UI",9)).pack(anchor="w",pady=(0,20))
        tk.Label(box,text="TÊN ĐĂNG NHẬP",bg="white",fg="#68758b",font=("Segoe UI",8,"bold")).pack(anchor="w"); self.luser=ttk.Entry(box,width=37); self.luser.insert(0,"admin"); self.luser.pack(pady=(5,14),ipady=5)
        tk.Label(box,text="MẬT KHẨU",bg="white",fg="#68758b",font=("Segoe UI",8,"bold")).pack(anchor="w"); self.lpass=ttk.Entry(box,width=37,show="*"); self.lpass.insert(0,"123456"); self.lpass.pack(pady=(5,16),ipady=5)
        ttk.Button(box,text="Đăng nhập  →",style="Accent.TButton",command=self.login).pack(fill="x")
        tk.Label(box,text="TÀI KHOẢN DÙNG THỬ\nQuản trị viên: admin / 123456\nNhân viên: nhanvien / 123456",bg="#f4f6fa",fg="#7b879b",font=("Segoe UI",8),justify="left",padx=11,pady=9).pack(fill="x",pady=14)
        ttk.Button(box,text="Tạo tài khoản nhân viên",command=self.register_account).pack(fill="x",pady=(0,8))
        self.lpass.bind("<Return>",lambda e:self.login())
    def login(self):
        try: self.user=self.service.login(self.luser.get().strip(),self.lpass.get())
        except Exception as e: return messagebox.showerror("Loi du lieu",str(e))
        if not self.user: return messagebox.showerror("Dang nhap","Sai ten dang nhap hoac mat khau")
        self.build()
    def admin(self): return self.user["role"]=="admin"
    def register_account(self):
        username=simpledialog.askstring("Tao tai khoan","Ten dang nhap (3-24 ky tu):",parent=self.root)
        if username is None: return
        name=simpledialog.askstring("Tao tai khoan","Ho va ten:",parent=self.root)
        password=simpledialog.askstring("Tao tai khoan","Mat khau (toi thieu 6 ky tu):",show="*",parent=self.root)
        if name is None or password is None: return
        try: self.service.create_user(username,password,name,"staff"); messagebox.showinfo("Tao tai khoan","Da tao tai khoan nhan vien. Ban co the dang nhap.")
        except Exception as e: messagebox.showerror("Khong the tao tai khoan",str(e))
    def change_password(self):
        old=simpledialog.askstring("Doi mat khau","Nhap mat khau hien tai:",show="*",parent=self.root)
        if old is None: return
        new=simpledialog.askstring("Doi mat khau","Nhap mat khau moi (toi thieu 6 ky tu):",show="*",parent=self.root)
        if new is None: return
        try: self.service.change_password(self.user["username"],old,new); messagebox.showinfo("Doi mat khau","Da cap nhat mat khau")
        except Exception as e: messagebox.showerror("Khong the doi mat khau",str(e))
    def logout(self):
        if messagebox.askyesno("Dang xuat","Ban muon dang xuat khoi he thong?"):
            self.user=None; self.show_login()
    def start_check_in(self):
        self.show_page("sessions")
        self.in_plate.focus_set()
    def build(self):
        self.clear(); self.root.configure(bg="#f4f6fa")
        shell=tk.Frame(self.root,bg="#f4f6fa"); shell.pack(fill="both",expand=True)
        side=tk.Frame(shell,bg="#17243a",width=238); side.pack(side="left",fill="y"); side.pack_propagate(False)
        brand=tk.Frame(side,bg="#17243a"); brand.pack(fill="x",pady=(23,27),padx=18)
        tk.Label(brand,text="P",bg="#536ff2",fg="white",font=("Segoe UI",16,"bold"),width=2,height=1).pack(side="left",ipady=4)
        tk.Label(brand,text="parkly",bg="#17243a",fg="white",font=("Segoe UI",18,"bold")).pack(side="left",padx=10)
        tk.Label(side,text="QUẢN LÝ BÃI ĐỖ XE",bg="#17243a",fg="#8492a9",font=("Segoe UI",8,"bold")).pack(anchor="w",padx=19,pady=(0,9))
        self.nav_buttons={}
        navitems=[("home","▦","Tổng quan"),("parking","▣","Sơ đồ bãi xe"),("vehicles","◉","Phương tiện"),("sessions","↔","Lượt gửi xe"),("reports","▤","Báo cáo"),("feedback","☆","Phản hồi khách hàng")]
        if self.admin(): navitems.append(("settings","⚙","Cài đặt"))
        for key,ico,label in navitems:
            b=tk.Button(side,text=f"{ico}    {label}",anchor="w",relief="flat",bd=0,bg="#17243a",fg="#bdc7d7",activebackground="#2a3954",activeforeground="white",font=("Segoe UI",10),padx=14,pady=11,command=lambda k=key:self.show_page(k))
            b.pack(fill="x",padx=10,pady=2); self.nav_buttons[key]=b
        userbox=tk.Frame(side,bg="#17243a"); userbox.pack(side="bottom",fill="x",padx=14,pady=16)
        tk.Frame(userbox,bg="#35435c",height=1).pack(fill="x",pady=(0,12))
        tk.Label(userbox,text=self.user["full_name"],bg="#17243a",fg="white",font=("Segoe UI",10,"bold")).pack(anchor="w")
        tk.Label(userbox,text="Quản trị viên" if self.admin() else "Nhân viên",bg="#17243a",fg="#acb9ce",font=("Segoe UI",8)).pack(anchor="w",pady=(3,0))
        main=tk.Frame(shell,bg="#f4f6fa"); main.pack(side="left",fill="both",expand=True)
        top=tk.Frame(main,bg="white",height=66,highlightbackground="#e7ebf2",highlightthickness=1); top.pack(fill="x"); top.pack_propagate(False)
        self.crumb=tk.Label(top,text="Parkly  /  Tổng quan",bg="white",fg="#7b879b",font=("Segoe UI",9)); self.crumb.pack(side="left",padx=28)
        tk.Label(top,text="●  HỆ THỐNG ĐANG HOẠT ĐỘNG",bg="white",fg="#138a67",font=("Segoe UI",8,"bold")).pack(side="right",padx=22)
        tk.Button(top,text="Đổi mật khẩu",command=self.change_password,bg="white",fg="#34435a",relief="solid",bd=1,font=("Segoe UI",9),padx=10,pady=5).pack(side="right",padx=4)
        tk.Button(top,text="Đăng xuất",command=self.logout,bg="white",fg="#34435a",relief="solid",bd=1,font=("Segoe UI",9),padx=10,pady=5).pack(side="right",padx=8)
        self.content=tk.Frame(main,bg="#f4f6fa"); self.content.pack(fill="both",expand=True)
        self.frames={}
        keys=["home","parking","vehicles","sessions","reports","feedback"]+( ["settings"] if self.admin() else [])
        for key in keys: self.frames[key]=ttk.Frame(self.content,padding=20,style="Page.TFrame")
        self.make_home(); self.make_parking(); self.make_vehicles(); self.make_sessions(); self.make_reports(); self.make_feedback()
        if self.admin(): self.make_settings()
        self.localize_widgets(); self.refresh(); self.show_page("home")

    def show_page(self,key):
        for frame in self.frames.values(): frame.pack_forget()
        self.frames[key].pack(fill="both",expand=True)
        labels={"home":"Tổng quan","parking":"Sơ đồ bãi xe","vehicles":"Phương tiện","sessions":"Lượt gửi xe","reports":"Báo cáo","feedback":"Phản hồi khách hàng","settings":"Cài đặt"}
        self.crumb.configure(text="Parkly  /  "+labels[key])
        for name,button in self.nav_buttons.items():
            button.configure(bg="#2a3954" if name==key else "#17243a",fg="white" if name==key else "#bdc7d7")
    def make_home(self):
        f=self.frames["home"]
        head=tk.Frame(f,bg="#f4f6fa"); head.pack(fill="x",pady=(0,15))
        left=tk.Frame(head,bg="#f4f6fa"); left.pack(side="left")
        tk.Label(left,text="TỔNG QUAN",bg="#f4f6fa",fg="#4568f5",font=("Segoe UI",8,"bold")).pack(anchor="w")
        tk.Label(left,text="Xin chào, "+self.user["full_name"]+"!",bg="#f4f6fa",fg="#17243a",font=("Segoe UI",21,"bold")).pack(anchor="w",pady=(3,0))
        tk.Label(left,text="Đây là tình hình bãi xe của bạn hôm nay.",bg="#f4f6fa",fg="#7b879b",font=("Segoe UI",9)).pack(anchor="w",pady=(3,0))
        actions=tk.Frame(head,bg="#f4f6fa"); actions.pack(side="right",anchor="s")
        tk.Button(actions,text="Sơ đồ bãi xe",command=lambda:self.show_page("parking"),bg="white",fg="#17243a",relief="solid",bd=1,font=("Segoe UI",9),padx=10,pady=7).pack(side="left",padx=4)
        tk.Button(actions,text="＋  Nhận xe",command=self.start_check_in,bg="#4568f5",fg="white",relief="flat",font=("Segoe UI",9,"bold"),padx=12,pady=8).pack(side="left",padx=4)
        cards=tk.Frame(f,bg="#f4f6fa"); cards.pack(fill="x",pady=(0,13)); self.metric_values={}
        for i,(key,label,ico) in enumerate([("slots","TONG SO VI TRI","▦"),("active","XE DANG GUI","◉"),("revenue","DOANH THU THANG","₫"),("today","LUOT XE HOM NAY","↔")]):
            card=tk.Frame(cards,bg="white",highlightbackground="#e7ebf2",highlightthickness=1,padx=14,pady=11); card.grid(row=0,column=i,sticky="nsew",padx=(0 if i==0 else 8,0)); cards.grid_columnconfigure(i,weight=1)
            tk.Label(card,text=label,bg="white",fg="#7b879b",font=("Segoe UI",8,"bold")).pack(anchor="w")
            val=tk.Label(card,text="0",bg="white",fg="#17243a",font=("Segoe UI",19,"bold")); val.pack(anchor="w",pady=(6,1)); self.metric_values[key]=val
            tk.Label(card,text=ico+"   Cap nhat truc tiep",bg="white",fg="#7b879b",font=("Segoe UI",8)).pack(anchor="w")
        middle=tk.Frame(f,bg="#f4f6fa"); middle.pack(fill="x",pady=(0,13))
        self.slot_panel=tk.Frame(middle,bg="white",highlightbackground="#e7ebf2",highlightthickness=1,padx=13,pady=11); self.slot_panel.pack(side="left",fill="both",expand=True,padx=(0,7))
        hdr=tk.Frame(self.slot_panel,bg="white"); hdr.pack(fill="x")
        tk.Label(hdr,text="So do bai xe",bg="white",fg="#17243a",font=("Segoe UI",11,"bold")).pack(side="left")
        tk.Label(hdr,text="Vi tri · cap nhat truc tiep",bg="white",fg="#7b879b",font=("Segoe UI",8)).pack(side="right")
        self.slot_grid=tk.Frame(self.slot_panel,bg="white"); self.slot_grid.pack(fill="x",pady=(9,1)); self.home_slot_widgets=[]
        self.util_panel=tk.Frame(middle,bg="white",width=285,highlightbackground="#e7ebf2",highlightthickness=1,padx=12,pady=11); self.util_panel.pack(side="right",fill="y",padx=(7,0)); self.util_panel.pack_propagate(False)
        tk.Label(self.util_panel,text="Mức độ sử dụng",bg="white",fg="#17243a",font=("Segoe UI",11,"bold")).pack(anchor="w")
        tk.Label(self.util_panel,text="Tỷ lệ lấp đầy hiện tại",bg="white",fg="#7b879b",font=("Segoe UI",8)).pack(anchor="w",pady=(3,8))
        self.util_canvas=tk.Canvas(self.util_panel,width=105,height=105,bg="white",highlightthickness=0); self.util_canvas.pack(side="left",padx=(0,9))
        self.util_legend=tk.Frame(self.util_panel,bg="white"); self.util_legend.pack(side="left",fill="y",expand=True)
        self.util_values=[]
        for label in ("Dang su dung","Con trong","Bao tri"):
            row=tk.Frame(self.util_legend,bg="white"); row.pack(fill="x",pady=7)
            tk.Label(row,text="●  "+label,bg="white",fg="#7b879b",font=("Segoe UI",8)).pack(side="left")
            val=tk.Label(row,text="0",bg="white",fg="#17243a",font=("Segoe UI",9,"bold")); val.pack(side="right"); self.util_values.append(val)
        recent=tk.Frame(f,bg="white",highlightbackground="#e7ebf2",highlightthickness=1,padx=11,pady=9); recent.pack(fill="both",expand=True)
        tk.Label(recent,text="Hoat dong gan day",bg="white",fg="#17243a",font=("Segoe UI",11,"bold")).pack(anchor="w",pady=(0,6))
        self.home_tree=self.tree(recent,("plate","type","slot","in","status","fee"),("Bien so","Loai xe","O do","Thoi gian vao","Trang thai","Phi / thao tac"),(115,90,60,145,100,120),4)
    def tree(self,parent,columns,headings,widths,height):
        wrap=tk.Frame(parent,bg="white"); wrap.pack(fill="both",expand=True)
        tree=ttk.Treeview(wrap,columns=columns,show="headings",height=height,selectmode="browse")
        vscroll=ttk.Scrollbar(wrap,orient="vertical",command=tree.yview)
        hscroll=ttk.Scrollbar(wrap,orient="horizontal",command=tree.xview)
        tree.configure(yscrollcommand=vscroll.set,xscrollcommand=hscroll.set)
        for col,title,width in zip(columns,headings,widths):
            tree.heading(col,text=VI_TEXT.get(title,title))
            tree.column(col,width=width,minwidth=70,anchor="w",stretch=True)
        tree.tag_configure("stripe",background="#f7f9fc")
        tree.grid(row=0,column=0,sticky="nsew"); vscroll.grid(row=0,column=1,sticky="ns"); hscroll.grid(row=1,column=0,sticky="ew")
        wrap.grid_rowconfigure(0,weight=1); wrap.grid_columnconfigure(0,weight=1)
        return tree
    def localize_widgets(self,parent=None):
        """Áp dụng nhãn tiếng Việt có dấu cho các widget và lựa chọn."""
        parent=parent or self.root
        for child in parent.winfo_children():
            try:
                text=child.cget("text")
                if text in VI_TEXT: child.configure(text=VI_TEXT[text])
            except (tk.TclError,AttributeError): pass
            if isinstance(child,ttk.Combobox):
                old=child.get(); values=child.cget("values")
                translated=[VI_TEXT.get(value,value) for value in values]
                child.configure(values=translated)
                if old: child.set(VI_TEXT.get(old,old))
            self.localize_widgets(child)
    def make_parking(self):
        f=self.frames["parking"]; ttk.Label(f,text="Quan ly vi tri do",style="Title.TLabel").pack(anchor="w")
        bar=ttk.Frame(f); bar.pack(fill="x",pady=8)
        ttk.Label(bar,text="Ma vi tri").pack(side="left",padx=(0,4)); self.slot_id=ttk.Entry(bar,width=12); self.slot_id.pack(side="left",padx=(0,10))
        ttk.Label(bar,text="Loai xe").pack(side="left",padx=(0,4)); self.slot_type=ttk.Combobox(bar,values=["Xe may","O to"],width=12,state="readonly"); self.slot_type.set("Xe may"); self.slot_type.pack(side="left",padx=(0,10))
        self.slot_add=ttk.Button(bar,text="Them o",command=self.add_slot); self.slot_add.pack(side="left",padx=3)
        self.slot_toggle=ttk.Button(bar,text="Bao tri / Mo lai",command=self.toggle_slot); self.slot_toggle.pack(side="left",padx=3)
        self.slot_delete=ttk.Button(bar,text="Xoa o trong",command=self.delete_slot); self.slot_delete.pack(side="left",padx=3)
        self.slot_tree=self.tree(f,("id","type","status","plate"),("Ma o","Loai xe","Trang thai","Xe dang do"),(100,140,140,150),14)
        if not self.admin():
            for w in (self.slot_id,self.slot_type,self.slot_add,self.slot_toggle,self.slot_delete): w.state(["disabled"])
    def make_vehicles(self):
        f=self.frames["vehicles"]; ttk.Label(f,text="Danh sach phuong tien",style="Title.TLabel").pack(anchor="w")
        search=ttk.Frame(f); search.pack(fill="x",pady=(7,5))
        ttk.Label(search,text="Tim theo bien so, chu xe hoac dien thoai").pack(side="left"); self.vehicle_query=ttk.Entry(search,width=33); self.vehicle_query.pack(side="left",padx=7); self.vehicle_query.bind("<KeyRelease>",lambda e:self.refresh_vehicles())
        bar=ttk.Frame(f); bar.pack(fill="x",pady=(0,8))
        fields=[]
        for label,width in (("Bien so",15),("Loai xe",10),("Chu xe",16),("Dien thoai",13)):
            box=ttk.Frame(bar); box.pack(side="left",padx=(0,8)); ttk.Label(box,text=label).pack(anchor="w")
            entry=ttk.Combobox(box,values=["Xe may","O to"],width=width,state="readonly") if label=="Loai xe" else ttk.Entry(box,width=width)
            if label=="Loai xe": entry.set("Xe may")
            entry.pack(anchor="w",pady=(2,0)); fields.append(entry)
        self.v_plate,self.v_type,self.v_owner,self.v_phone=fields
        self.v_add=ttk.Button(bar,text="Them xe",command=self.add_vehicle); self.v_add.pack(side="left",padx=4,pady=(16,0))
        self.v_update=ttk.Button(bar,text="Cap nhat chon",command=self.update_vehicle); self.v_update.pack(side="left",padx=4,pady=(16,0))
        self.v_delete=ttk.Button(bar,text="Xoa xe",command=self.delete_vehicle); self.v_delete.pack(side="left",padx=4,pady=(16,0))
        self.vehicle_tree=self.tree(f,("plate","type","owner","phone","status"),("Bien so","Loai xe","Chu xe","Dien thoai","Tinh trang"),(140,100,170,120,140),12)
        self.vehicle_tree.bind("<<TreeviewSelect>>",self.select_vehicle)
        if not self.admin():
            for w in (self.v_plate,self.v_type,self.v_owner,self.v_phone,self.v_add,self.v_update,self.v_delete): w.state(["disabled"])
    def make_sessions(self):
        f=self.frames["sessions"]; ttk.Label(f,text="Nhan xe va luot gui",style="Title.TLabel").pack(anchor="w")
        bar=ttk.Frame(f); bar.pack(fill="x",pady=8)
        def field(parent,label,width,values=None):
            box=ttk.Frame(parent); box.pack(side="left",padx=(0,8)); ttk.Label(box,text=label).pack(anchor="w")
            entry=ttk.Combobox(box,values=values,width=width,state="readonly") if values else ttk.Entry(box,width=width)
            if values: entry.set(values[0])
            entry.pack(anchor="w",pady=(2,0)); return entry
        self.in_plate=field(bar,"Bien so xe",17); self.in_type=field(bar,"Loai xe",11,["Xe may","O to"])
        self.in_owner=field(bar,"Chu xe (khong bat buoc)",17); self.in_phone=field(bar,"Dien thoai",13)
        ttk.Button(bar,text="Nhan xe vao",style="Accent.TButton",command=self.check_in).pack(side="left",padx=4,pady=(16,0))
        ttk.Button(bar,text="Tra xe dang chon",command=self.check_out).pack(side="left",padx=4,pady=(16,0))
        filters=ttk.Frame(f); filters.pack(fill="x",pady=(2,5))
        ttk.Label(filters,text="Tim bien so / ma o").pack(side="left")
        self.session_query=ttk.Entry(filters,width=24); self.session_query.pack(side="left",padx=(5,12)); self.session_query.bind("<KeyRelease>",lambda e:self.refresh_sessions())
        ttk.Label(filters,text="Trang thai").pack(side="left")
        self.session_filter=ttk.Combobox(filters,values=["Tat ca","Dang gui","Da thanh toan"],width=16,state="readonly"); self.session_filter.set("Tat ca"); self.session_filter.pack(side="left",padx=5); self.session_filter.bind("<<ComboboxSelected>>",lambda e:self.refresh_sessions())
        self.session_tree=self.tree(f,("id","plate","type","slot","in","out","status","fee"),("Ma luot","Bien so","Loai xe","O","Gio vao","Gio ra","Trang thai","Phi VND"),(95,120,90,55,150,150,100,100),11)
    def make_reports(self):
        f=self.frames["reports"]; ttk.Label(f,text="Bao cao doanh thu",style="Title.TLabel").pack(anchor="w")
        bar=ttk.Frame(f); bar.pack(fill="x",pady=8)
        ttk.Label(bar,text="Tu ngay").pack(side="left"); self.date_from=ttk.Entry(bar,width=12); self.date_from.insert(0,date.today().replace(day=1).isoformat()); self.date_from.pack(side="left",padx=4)
        ttk.Label(bar,text="Den ngay").pack(side="left"); self.date_to=ttk.Entry(bar,width=12); self.date_to.insert(0,date.today().isoformat()); self.date_to.pack(side="left",padx=4)
        ttk.Button(bar,text="Thong ke",command=self.refresh_report).pack(side="left",padx=4)
        self.currency=ttk.Combobox(bar,values=CURRENCIES,width=8,state="readonly"); self.currency.set("USD"); self.currency.pack(side="left",padx=4)
        ttk.Button(bar,text="Lay ty gia API",command=self.fetch_rate).pack(side="left",padx=4); ttk.Button(bar,text="Xuat CSV",command=self.export_csv).pack(side="left",padx=4)
        self.report_text=ttk.Label(f,text="",padding=12,background="white"); self.report_text.pack(fill="x",pady=8)
        self.report_tree=self.tree(f,("plate","type","slot","in","out","fee"),("Bien so","Loai xe","O","Vao","Ra","Phi VND"),(130,100,60,160,160,110),10)
    def make_feedback(self):
        f=self.frames["feedback"]; ttk.Label(f,text="Phan hoi khach hang",style="Title.TLabel").pack(anchor="w")
        ttk.Label(f,text="Ghi nhan y kien, theo doi danh gia va gui phan hoi tu bai xe.").pack(anchor="w",pady=(3,10))
        form=ttk.LabelFrame(f,text="Ghi nhan danh gia moi",padding=10); form.pack(fill="x",pady=(0,10))
        line=ttk.Frame(form); line.pack(fill="x")
        ttk.Label(line,text="Ten khach").pack(side="left"); self.fb_name=ttk.Entry(line,width=20); self.fb_name.pack(side="left",padx=5)
        ttk.Label(line,text="Bien so (tuy chon)").pack(side="left"); self.fb_plate=ttk.Entry(line,width=15); self.fb_plate.pack(side="left",padx=5)
        ttk.Label(line,text="Nhom").pack(side="left"); self.fb_category=ttk.Combobox(line,values=["Nhan vien","Co so vat chat","An toan","Thanh toan","Khac"],width=17,state="readonly"); self.fb_category.set("Nhan vien"); self.fb_category.pack(side="left",padx=5)
        ttk.Label(line,text="Sao").pack(side="left"); self.fb_rating=ttk.Combobox(line,values=[1,2,3,4,5],width=4,state="readonly"); self.fb_rating.set(5); self.fb_rating.pack(side="left",padx=5)
        row=ttk.Frame(form); row.pack(fill="x",pady=(8,0)); ttk.Label(row,text="Noi dung").pack(side="left"); self.fb_comment=ttk.Entry(row); self.fb_comment.pack(side="left",fill="x",expand=True,padx=5); ttk.Button(row,text="Luu phan hoi",command=self.add_feedback).pack(side="left",padx=4)
        tools=ttk.Frame(f); tools.pack(fill="x",pady=(0,6)); ttk.Label(tools,text="Tim ten, bien so hoac noi dung").pack(side="left"); self.fb_query=ttk.Entry(tools,width=30); self.fb_query.pack(side="left",padx=6); self.fb_query.bind("<KeyRelease>",lambda e:self.refresh_feedback()); ttk.Button(tools,text="Tra loi chon",command=self.reply_feedback).pack(side="left",padx=3); ttk.Button(tools,text="Xoa chon",command=self.delete_feedback).pack(side="left",padx=3)
        self.feedback_tree=self.tree(f,("id","date","name","plate","category","rating","comment","reply"),("Ma","Ngay gui","Khach hang","Bien so","Nhom","Sao","Noi dung","Phan hoi bai xe"),(110,145,150,120,130,55,280,260),10)
    def refresh_feedback(self):
        if not hasattr(self,"feedback_tree"): return
        q=self.fb_query.get().strip().casefold()
        rows=[]
        for x in reversed(self.service.data.get("feedback",[])):
            text=" ".join(str(x.get(k,"")) for k in ("customer_name","plate","category","comment","reply")).casefold()
            if not q or q in text: rows.append((x["feedback_id"],x["created_at"][:16].replace("T"," "),x["customer_name"],x.get("plate",""),VI_TEXT.get(x["category"],x["category"]),"★"*x["rating"],x["comment"],x.get("reply", "Chưa phản hồi")))
        self.fill(self.feedback_tree,rows)
    def add_feedback(self):
        try:
            self.service.add_feedback(self.fb_name.get(),CATEGORY_CODE.get(self.fb_category.get(),self.fb_category.get()),int(self.fb_rating.get()),self.fb_comment.get(),self.fb_plate.get()); self.fb_name.delete(0,"end"); self.fb_plate.delete(0,"end"); self.fb_comment.delete(0,"end"); self.refresh_feedback(); messagebox.showinfo("Phản hồi","Đã ghi nhận đánh giá khách hàng")
        except Exception as e: messagebox.showerror("Du lieu chua hop le",str(e))
    def reply_feedback(self):
        row=self.selected(self.feedback_tree)
        if not row: return messagebox.showwarning("Chon phan hoi","Hay chon danh gia can tra loi")
        reply=simpledialog.askstring("Tra loi khach hang","Nhap noi dung phan hoi:",parent=self.root)
        if reply is None: return
        try: self.service.reply_feedback(row[0],reply,self.user["username"]); self.refresh_feedback(); messagebox.showinfo("Phan hoi","Da luu loi tra loi")
        except Exception as e: messagebox.showerror("Khong the tra loi",str(e))
    def delete_feedback(self):
        row=self.selected(self.feedback_tree)
        if not row: return messagebox.showwarning("Chon phan hoi","Hay chon danh gia can xoa")
        if not self.admin(): return messagebox.showwarning("Phan quyen","Chi quan tri vien duoc xoa phan hoi")
        if messagebox.askyesno("Xac nhan","Xoa danh gia cua "+row[2]+"?"):
            try: self.service.delete_feedback(row[0]); self.refresh_feedback()
            except Exception as e: messagebox.showerror("Khong the xoa",str(e))
    def make_settings(self):
        f=self.frames["settings"]; ttk.Label(f,text="Cau hinh he thong",style="Title.TLabel").pack(anchor="w",pady=(0,10))
        price_panel=tk.Frame(f,bg="white",highlightbackground="#e7ebf2",highlightthickness=1,padx=14,pady=11); price_panel.pack(fill="x",pady=(0,10))
        tk.Label(price_panel,text="Don gia gui xe",bg="white",fg="#17243a",font=("Segoe UI",11,"bold")).pack(anchor="w",pady=(0,7))
        bar=ttk.Frame(price_panel); bar.pack(fill="x")
        ttk.Label(bar,text="Xe may VND/gio").pack(side="left"); self.bike=ttk.Entry(bar,width=12); self.bike.insert(0,str(self.service.prices["Xe may"])); self.bike.pack(side="left",padx=5)
        ttk.Label(bar,text="O to VND/gio").pack(side="left",padx=(12,0)); self.car=ttk.Entry(bar,width=12); self.car.insert(0,str(self.service.prices["O to"])); self.car.pack(side="left",padx=5)
        ttk.Button(bar,text="Luu gia",command=self.save_prices).pack(side="left",padx=5)
        create=tk.Frame(f,bg="white",highlightbackground="#e7ebf2",highlightthickness=1,padx=14,pady=11); create.pack(fill="x",pady=(0,10))
        tk.Label(create,text="Tao tai khoan",bg="white",fg="#17243a",font=("Segoe UI",11,"bold")).pack(anchor="w",pady=(0,7))
        row=ttk.Frame(create); row.pack(fill="x")
        def account_field(label,width,secret=False,values=None):
            box=ttk.Frame(row); box.pack(side="left",padx=(0,9)); ttk.Label(box,text=label).pack(anchor="w")
            entry=ttk.Combobox(box,values=values,width=width,state="readonly") if values else ttk.Entry(box,width=width,show="*" if secret else "")
            if values: entry.set(values[0])
            entry.pack(anchor="w",pady=(2,0)); return entry
        self.new_username=account_field("Ten dang nhap",16)
        self.new_password=account_field("Mat khau (6+ ky tu)",15,secret=True)
        self.new_name=account_field("Ho ten",20)
        self.new_role=account_field("Vai tro",10,values=["staff","admin"])
        ttk.Button(row,text="Tao tai khoan",command=self.add_user).pack(side="left",padx=4,pady=(16,0))
        users=tk.Frame(f,bg="white",highlightbackground="#e7ebf2",highlightthickness=1,padx=12,pady=9); users.pack(fill="both",expand=True)
        tk.Label(users,text="Tai khoan va phan quyen",bg="white",fg="#17243a",font=("Segoe UI",11,"bold")).pack(anchor="w",pady=(0,5))
        self.user_tree=self.tree(users,("username","name","role"),("Ten dang nhap","Ho ten","Vai tro"),(190,260,150),5)
        actions=ttk.Frame(users); actions.pack(fill="x",pady=(6,0))
        ttk.Label(actions,text="Mat khau moi (de trong neu khong doi)").pack(side="left",padx=(0,5))
        self.user_new_password=ttk.Entry(actions,width=20,show="*"); self.user_new_password.pack(side="left",padx=5)
        self.user_new_role=ttk.Combobox(actions,values=["staff","admin"],width=10,state="readonly"); self.user_new_role.set("staff"); self.user_new_role.pack(side="left",padx=5)
        ttk.Button(actions,text="Cap nhat tai khoan chon",command=self.update_user).pack(side="left",padx=5)
        ttk.Button(actions,text="Xoa tai khoan chon",command=self.delete_user).pack(side="left",padx=5)
        tools=ttk.Frame(f); tools.pack(fill="x",pady=8)
        ttk.Button(tools,text="Tao 5 xe demo ngau nhien",command=self.make_random).pack(side="left",padx=3)
        ttk.Button(tools,text="Sao luu JSON",command=self.export_json).pack(side="left",padx=3)
        ttk.Button(tools,text="Khoi phuc JSON",command=self.import_json).pack(side="left",padx=3)
        ttk.Label(f,text=f"Tep du lieu: {DATA_FILE}\nMat khau demo: admin/123456 va nhanvien/123456",wraplength=850).pack(anchor="w",pady=10)
    def refresh(self):
        self.refresh_home(); self.refresh_slots(); self.refresh_vehicles(); self.refresh_sessions(); self.refresh_report(); self.refresh_users(); self.refresh_feedback()
    def refresh_home(self):
        d=self.service.data; active=[s for s in d["sessions"] if s["status"]=="active"]
        month=date.today().strftime("%Y-%m"); income=sum(s["fee"] for s in d["sessions"] if s["status"]=="closed" and s["check_out"].startswith(month))
        if hasattr(self,"metric_values"):
            self.metric_values["slots"].configure(text=str(len(d["slots"])))
            self.metric_values["active"].configure(text=str(len(active)))
            self.metric_values["revenue"].configure(text=f"{income:,.0f} VND")
            self.metric_values["today"].configure(text=str(sum(s["check_in"][:10]==date.today().isoformat() for s in d["sessions"])))
            slots=d["slots"]
            for widget in self.home_slot_widgets: widget.destroy()
            self.home_slot_widgets=[]
            for i,s in enumerate(slots[:18]):
                state=s["status"]; car=next((x["plate"] for x in active if x["slot_id"]==s["slot_id"]),"")
                bg,edge=("#f0faf5","#dcefe5") if state=="free" else (("#fff7e8","#f1ddb6") if state=="occupied" else ("#f1f2f5","#e3e5ea"))
                card=tk.Frame(self.slot_grid,bg=bg,highlightbackground=edge,highlightthickness=1,padx=5,pady=4,height=48)
                card.grid(row=i//6,column=i%6,sticky="nsew",padx=3,pady=3); self.slot_grid.grid_columnconfigure(i%6,weight=1); card.grid_propagate(False)
                tk.Label(card,text=s["slot_id"],bg=bg,fg="#17243a",font=("Segoe UI",8,"bold")).pack(anchor="w")
                tk.Label(card,text=car or show_status(state),bg=bg,fg="#7b879b",font=("Segoe UI",7)).pack(anchor="w")
                self.home_slot_widgets.append(card)
            total=len(slots); used=len(active); fill=round(used/total*100) if total else 0
            self.util_canvas.delete("all")
            self.util_canvas.create_oval(10,10,100,100,outline="#e7ebf2",width=12)
            if fill: self.util_canvas.create_arc(10,10,100,100,start=90,extent=-fill*3.6,style="arc",outline="#4c68f5",width=12)
            self.util_canvas.create_text(55,48,text=f"{fill}%",fill="#17243a",font=("Segoe UI",15,"bold"))
            self.util_canvas.create_text(55,67,text=f"{used}/{total} chỗ",fill="#7b879b",font=("Segoe UI",7))
            self.util_values[0].configure(text=str(used)); self.util_values[1].configure(text=str(sum(s["status"]=="free" for s in slots))); self.util_values[2].configure(text=str(sum(s["status"]=="maintenance" for s in slots)))
            recent=sorted(d["sessions"],key=lambda x:x["check_in"],reverse=True)[:6]
        self.fill(self.home_tree,[(s["plate"],show_vehicle(s["vehicle_type"]),s["slot_id"],s["check_in"][:16].replace("T"," "),show_status(s["status"]),f"{s['fee']:,} VND" if s["status"]=="closed" else "Trả xe") for s in recent])
    def refresh_slots(self):
        active=self.service.data["sessions"]
        self.fill(self.slot_tree,[(s["slot_id"],show_vehicle(s["vehicle_type"]),show_status(s["status"]),next((x["plate"] for x in active if x["slot_id"]==s["slot_id"] and x["status"]=="active"),"")) for s in self.service.data["slots"]])
    def refresh_vehicles(self):
        if not hasattr(self,"vehicle_tree"): return
        q=self.vehicle_query.get().lower().strip(); active=[s["plate"] for s in self.service.data["sessions"] if s["status"]=="active"]
        self.fill(self.vehicle_tree,[(v["plate"],show_vehicle(v["vehicle_type"]),v.get("owner",""),v.get("phone",""),"Đang gửi" if v["plate"] in active else "Ngoài bãi") for v in self.service.data["vehicles"] if q in (v["plate"]+v.get("owner","")+v.get("phone","")).lower()])
    def refresh_sessions(self):
        if not hasattr(self,"session_tree"): return
        q=self.session_query.get().lower().strip(); rows=list(reversed(self.service.data["sessions"]))
        choice=self.session_filter.get() if hasattr(self,"session_filter") else "Tất cả"
        status_filter={"Đang gửi":"active","Đã thanh toán":"closed"}.get(choice)
        self.fill(self.session_tree,[(s["session_id"],s["plate"],show_vehicle(s["vehicle_type"]),s["slot_id"],s["check_in"][:19].replace("T"," "),s.get("check_out","")[:19].replace("T"," "),show_status(s["status"]),s["fee"]) for s in rows if q in (s["plate"]+s["slot_id"]+s["status"]).lower() and (not status_filter or s["status"]==status_filter)])
    def refresh_users(self):
        if hasattr(self,"user_tree"):
            self.fill(self.user_tree,[(u["username"],u["full_name"],"Quản trị viên" if u["role"]=="admin" else "Nhân viên") for u in self.service.data["users"]])
    @staticmethod
    def fill(tree,rows):
        tree.delete(*tree.get_children())
        for index,row in enumerate(rows): tree.insert("","end",values=row,tags=("stripe" if index%2 else "",))
    def refresh_report(self):
        if not hasattr(self,"report_tree"): return
        try: rows,total=self.service.get_revenue(self.date_from.get().strip(),self.date_to.get().strip())
        except Exception as e: return messagebox.showerror("Bao cao",str(e))
        c=self.currency.get() or "USD"; rate=self.service.data["rates"].get(c)
        converted=f" | {c}: {total*rate['rate']:,.2f} (tỷ giá {rate['rate']})" if rate else f" | Chưa có tỷ giá {c}"
        self.report_text.configure(text=f"{len(rows)} lượt đã thanh toán     Doanh thu: {total:,} VND{converted}")
        self.fill(self.report_tree,[(s["plate"],show_vehicle(s["vehicle_type"]),s["slot_id"],s["check_in"][:19],s["check_out"][:19],s["fee"]) for s in rows])
    def selected(self,tree):
        sel=tree.selection(); return tree.item(sel[0],"values") if sel else None
    def add_vehicle(self):
        try: self.service.add_vehicle(self.v_plate.get(),VEHICLE_CODE.get(self.v_type.get(),self.v_type.get()),self.v_owner.get(),self.v_phone.get()); self.refresh(); messagebox.showinfo("Phuong tien","Da them phuong tien")
        except Exception as e: messagebox.showerror("Khong the them",str(e))
    def select_vehicle(self,event=None):
        row=self.selected(self.vehicle_tree)
        if row:
            for entry,value in ((self.v_plate,row[0]),(self.v_owner,row[2]),(self.v_phone,row[3])): entry.delete(0,"end"); entry.insert(0,value)
            self.v_type.set(row[1])
    def update_vehicle(self):
        row=self.selected(self.vehicle_tree)
        if not row: return messagebox.showwarning("Chon xe","Chon dong can cap nhat")
        try: self.service.update_vehicle(row[0],self.v_plate.get(),VEHICLE_CODE.get(self.v_type.get(),self.v_type.get()),self.v_owner.get(),self.v_phone.get()); self.refresh()
        except Exception as e: messagebox.showerror("Khong the cap nhat",str(e))
    def delete_vehicle(self):
        row=self.selected(self.vehicle_tree)
        if not row: return messagebox.showwarning("Chon xe","Chon dong can xoa")
        if messagebox.askyesno("Xac nhan","Xoa xe "+row[0]+"?"):
            try: self.service.delete_vehicle(row[0]); self.refresh()
            except Exception as e: messagebox.showerror("Khong the xoa",str(e))
    def add_slot(self):
        try: self.service.add_slot(self.slot_id.get(),VEHICLE_CODE.get(self.slot_type.get(),self.slot_type.get())); self.refresh(); messagebox.showinfo("Vi tri","Da them o do")
        except Exception as e: messagebox.showerror("Khong the them",str(e))
    def delete_slot(self):
        row=self.selected(self.slot_tree)
        if not row: return messagebox.showwarning("Chon vi tri","Hay chon o muon xoa")
        if not messagebox.askyesno("Xac nhan","Xoa vi tri "+row[0]+"? Chi xoa duoc o chua co lich su."): return
        try: self.service.delete_slot(row[0]); self.refresh()
        except Exception as e: messagebox.showerror("Khong the xoa",str(e))
    def toggle_slot(self):
        row=self.selected(self.slot_tree)
        if not row: return messagebox.showwarning("Chon o","Chon vi tri can cap nhat")
        try: self.service.toggle_maintenance(row[0]); self.refresh()
        except Exception as e: messagebox.showerror("Khong the cap nhat",str(e))
    def check_in(self):
        try:
            s=self.service.check_in(self.in_plate.get(),VEHICLE_CODE.get(self.in_type.get(),self.in_type.get()),self.in_owner.get(),self.in_phone.get()); self.refresh()
            self.in_plate.delete(0,"end"); self.in_owner.delete(0,"end"); self.in_phone.delete(0,"end")
            messagebox.showinfo("Nhan xe",f"Da nhan {s['plate']} vao vi tri {s['slot_id']}")
        except Exception as e: messagebox.showerror("Khong the nhan xe",str(e))
    def check_out(self):
        row=self.selected(self.session_tree)
        if not row: return messagebox.showwarning("Chon luot","Chon luot gui dang mo")
        if row[6]!="Đang gửi": return messagebox.showwarning("Trạng thái","Lượt này đã được thanh toán")
        try:
            s,hours=self.service.check_out(row[0]); self.refresh()
            rate=s.get("hourly_rate",self.service.prices[s["vehicle_type"]])
            messagebox.showinfo("Thanh toan",f"Bien so: {s['plate']}\nSo gio tinh phi: {hours}\nDon gia: {rate:,} VND/gio\nTong phi: {s['fee']:,} VND")
        except Exception as e: messagebox.showerror("Khong the tra xe",str(e))
    def save_prices(self):
        try: self.service.set_prices(int(self.bike.get()),int(self.car.get())); messagebox.showinfo("Cau hinh","Da luu don gia")
        except Exception as e: messagebox.showerror("Don gia khong hop le",str(e))
    def add_user(self):
        try: self.service.create_user(self.new_username.get().strip(),self.new_password.get(),self.new_name.get().strip(),"admin" if self.new_role.get() in ("admin","Quản trị viên") else "staff"); self.refresh_users(); messagebox.showinfo("Tai khoan","Da tao tai khoan")
        except Exception as e: messagebox.showerror("Khong the tao tai khoan",str(e))
    def update_user(self):
        row=self.selected(self.user_tree)
        if not row: return messagebox.showwarning("Chon tai khoan","Hay chon tai khoan can cap nhat")
        try:
            self.service.update_user(row[0],self.user_new_password.get(),"admin" if self.user_new_role.get() in ("admin","Quản trị viên") else "staff",self.user["username"]); self.user_new_password.delete(0,"end"); self.refresh_users()
            messagebox.showinfo("Tai khoan","Da cap nhat vai tro/mat khau")
        except Exception as e: messagebox.showerror("Khong the cap nhat",str(e))
    def delete_user(self):
        row=self.selected(self.user_tree)
        if not row: return messagebox.showwarning("Chon tai khoan","Hay chon tai khoan can xoa")
        if not messagebox.askyesno("Xac nhan","Xoa tai khoan "+row[0]+"?"): return
        try: self.service.delete_user(row[0],self.user["username"]); self.refresh_users()
        except Exception as e: messagebox.showerror("Khong the xoa",str(e))
    def fetch_rate(self):
        try:
            c=self.currency.get(); r=self.service.fetch_rate(c); self.refresh_report()
            messagebox.showinfo("Ty gia",f"1 VND = {r['rate']} {c}\nCap nhat: {r['updated_at']}\nNguon: {r['source']}")
        except Exception as e: messagebox.showerror("Loi API","Khong lay duoc ty gia. Bao cao VND van hoat dong.\n"+str(e))
    def export_csv(self):
        try: rows,total=self.service.get_revenue(self.date_from.get().strip(),self.date_to.get().strip())
        except Exception as e: return messagebox.showerror("Bao cao",str(e))
        path=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")],initialfile="bao_cao_bai_do.csv")
        if not path: return
        try:
            with open(path,"w",newline="",encoding="utf-8-sig") as f:
                w=csv.writer(f); w.writerow(["Ma luot","Bien so","Loai xe","Vi tri","Gio vao","Gio ra","Phi VND"])
                for s in rows: w.writerow([s["session_id"],s["plate"],s["vehicle_type"],s["slot_id"],s["check_in"],s["check_out"],s["fee"]])
            messagebox.showinfo("Xuat bao cao",f"Da xuat {len(rows)} luot, tong {total:,} VND")
        except OSError as e: messagebox.showerror("Loi tep",str(e))
    def export_json(self):
        path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON","*.json")],initialfile="parkly_backup.json")
        if not path: return
        try:
            with open(path,"w",encoding="utf-8") as f: json.dump(self.service.data,f,ensure_ascii=False,indent=2)
            messagebox.showinfo("Sao luu","Da luu ban sao JSON")
        except OSError as e: messagebox.showerror("Loi sao luu",str(e))
    def import_json(self):
        path=filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not path or not messagebox.askyesno("Khoi phuc","Du lieu hien tai se duoc sao luu truoc. Tiep tuc?"): return
        try: self.service.data=self.storage.restore(path); self.service.prices=self.service.data["prices"]; self.refresh(); messagebox.showinfo("Khoi phuc","Da nhap du lieu")
        except Exception as e: messagebox.showerror("Khong the khoi phuc",str(e))
    def make_random(self):
        self.service.generate_demo_vehicles(5); self.refresh(); messagebox.showinfo("Du lieu mau","Da them 5 phuong tien ngau nhien")

