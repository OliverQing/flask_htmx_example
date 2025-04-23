document.addEventListener('htmx:afterSettle', function() {
    const forms = $('#form_div form');
    // 查找 aria-valid="false" 的 div 元素
    const invalidDivs = $('#form_div div[aria-valid="false"]');

    // 获取按钮元素，这里假设按钮的 id 是 submitButton，你可以根据实际情况修改
    const submitButton = $('#submit_button');

    if (invalidDivs.length > 0) {
        // 如果找到了 aria-valid="false" 的 div 元素，给按钮添加 disabled 属性
        submitButton.prop('disabled', true);
    } else {
        // 如果没有找到，移除按钮的 disabled 属性
        submitButton.prop('disabled', false);
    }
});
