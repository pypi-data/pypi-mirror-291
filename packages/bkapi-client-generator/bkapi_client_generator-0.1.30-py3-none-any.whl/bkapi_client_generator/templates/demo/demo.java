 public static void main(String[] args) {
        try {
            Client client = new Client("https://test.api.example.com/prod/");

            // Build request parameters
            RequestParams params = new RequestParams.Builder()
                    .setData(Map.of())  // 设置请求参数
                    .setPathParams(Map.of())  // 设置路径参数
                    .setQueryParams(Map.of())  // 设置 querystring
                    .setHeaders(Map.of())  // 设置请求头
                    .setTimeout(10)  // 设置超时
                    .setBkAppCode("x")  // 设置应用认证
                    .setBkAppSecret("y")  // 设置应用认证
                    .setBkToken("z")  // 设置用户认证
                    .setBkTicket("z")  // 内部版
                    .setBkUserName("z")  // 设置用户名
                    .build();

            // Make the request
            Response response = client.AnythingGet(params);
            // Handle the response
            if (response.isSuccessful()) {
                System.out.println("Response: " + response.body().string());
            } else {
                System.err.println("Request failed: " + response.code());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }