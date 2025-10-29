// 简单的API测试脚本
const axios = require('axios');

// 测试前端API服务层
async function testAPIServices() {
  console.log('=== 测试前端API服务层 ===');
  
  try {
    // 测试贴吧列表API
    console.log('1. 测试贴吧列表API...');
    const tiebaResponse = await axios.get('http://127.0.0.1:8000/api/tiebas/', {
      headers: { 'Content-Type': 'application/json' }
    });
    console.log('✅ 贴吧列表API测试成功:', tiebaResponse.data);
    
    // 测试用户认证API
    console.log('2. 测试用户认证API...');
    const authResponse = await axios.get('http://127.0.0.1:8000/api/auth/profile/', {
      headers: { 'Content-Type': 'application/json' }
    });
    console.log('✅ 用户认证API测试成功:', authResponse.data);
    
  } catch (error) {
    console.log('❌ API测试失败:', error.message);
    
    if (error.response) {
      console.log('状态码:', error.response.status);
      console.log('响应数据:', error.response.data);
    }
  }
}

// 运行测试
testAPIServices();