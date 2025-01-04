const button = document.getElementById('convertButton');  
        const input = document.getElementById('numberInput');  

        button.addEventListener('click', () => {  
            // 隐藏按钮，显示输入框  
            button.style.display = 'none';  
            input.style.display = 'inline';  
            input.focus(); // 聚焦到输入框  
        });  