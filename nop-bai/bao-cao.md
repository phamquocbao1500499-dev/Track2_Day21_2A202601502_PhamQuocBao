# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Phạm Quốc Bảo |
| MSSV | 2A202601502 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/phamquocbao1500499-dev/Track2_Day21_2A202601502_PhamQuocBao |
| Ngày nộp | 2026-08-22 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Bộ tham số này đạt f1_score cao nhất (0.7149) trong 3 lần thí nghiệm. Lần chạy 2 có accuracy cao nhưng f1_score thấp hơn nhiều, cho thấy mô hình bỏ sót nhiều trường hợp thu nhập cao. Quan sát thấy khi tăng n_estimators và max_depth thì f1 cải thiện, nhưng learning_rate thấp quá (0.05) làm giảm khả năng học của mô hình.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Adult có phân bố lớp mất cân bằng: chỉ 24.8% mẫu thuộc lớp thu nhập cao (>50K). Một mô hình luôn trả lời "thu nhập thấp" cho mọi đầu vào sẽ đạt accuracy 75.2% mà không học được gì. F1 của lớp dương đo khả năng bắt được các trường hợp thu nhập cao - điều mà accuracy không phản ánh. Không dùng average="weighted" hay average="macro" vì chúng bị lớp đa số kéo lên cao, che khuất vấn đề thực sự.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| DVC pull lỗi 401 Invalid Credentials | DVC không đọc GOOGLE_APPLICATION_CREDENTIALS từ env | Dùng `gcloud auth activate-service-account` trong CI |
| SSH deploy lỗi permission denied | Service account thiếu quyền compute | Thêm role compute.instanceAdmin.v1 và iam.serviceAccountUser |
| Systemd service lỗi bad unit file | Dấu ' trong username Lil'Pao0 không được escape | Tạo user labuser mới không có dấu ' |
| API lỗi FileNotFoundError model | serve.py dùng ~/models nhưng model ở /opt/income-api/models | Thêm biến MODEL_PATH vào service environment |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7149 | 0.8740 |
| Bước 3 (thêm `train_batch2`) | 0.2963 | 0.5250 |

**Nhận xét:** F1 giảm mạnh từ 0.7149 xuống 0.2963 khi thêm dữ liệu mới. Nguyên nhân là do train_batch2 được tạo bằng cách append trực tiếp vào train_batch1 mà không theo tỷ lệ phân bố gốc 75/25. Hệ quả là dữ liệu huấn luyện mới có phân bố lệch, làm mô hình không học được pattern đúng. Điều này cho thấy thêm dữ liệu không phải lúc nào cũng tốt - quan trọng là chất lượng và tính nhất quán của dữ liệu.

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___
