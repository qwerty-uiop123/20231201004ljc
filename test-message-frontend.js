// 前端消息功能测试脚本
// 在浏览器控制台中运行此脚本测试消息功能

async function testMessageFrontend() {
    console.log('开始测试前端消息功能...');
    
    // 测试对话列表API
    try {
        console.log('1. 测试对话列表API...');
        const conversationsResponse = await fetch('http://127.0.0.1:8000/api/chat/conversations/', {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                'Content-Type': 'application/json'
            }
        });
        
        if (conversationsResponse.ok) {
            const conversationsData = await conversationsResponse.json();
            console.log('对话列表API测试成功:', conversationsData);
            console.log('对话数量:', conversationsData.count);
        } else {
            console.error('对话列表API测试失败:', conversationsResponse.status);
        }
    } catch (error) {
        console.error('对话列表API测试异常:', error);
    }
    
    // 测试发送私信API
    try {
        console.log('2. 测试发送私信API...');
        const formData = new FormData();
        formData.append('recipient_id', '1');
        formData.append('content', '前端测试消息');
        formData.append('message_type', 'text');
        
        const sendResponse = await fetch('http://127.0.0.1:8000/api/chat/send/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            },
            body: formData
        });
        
        if (sendResponse.ok) {
            const sendData = await sendResponse.json();
            console.log('发送私信API测试成功:', sendData);
        } else {
            console.error('发送私信API测试失败:', sendResponse.status);
        }
    } catch (error) {
        console.error('发送私信API测试异常:', error);
    }
    
    console.log('前端消息功能测试完成');
}

// 检查是否已登录
function checkLoginStatus() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        console.warn('未检测到登录状态，请先登录');
        return false;
    }
    return true;
}

// 运行测试
if (checkLoginStatus()) {
    testMessageFrontend();
} else {
    console.log('请先登录系统');
}