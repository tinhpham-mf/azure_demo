# Sử dụng Node.js base image
FROM node:16.17.0

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép package.json và package-lock.json vào container
COPY package*.json ./

# Cài đặt các thư viện cần thiết
RUN npm install

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Xây dựng ứng dụng React
RUN npm run build

# Cài đặt `serve` để phục vụ nội dung build
RUN npm install -g serve

# Lệnh chạy ứng dụng React
CMD ["serve", "-s", "build", "-l", "3000"]
