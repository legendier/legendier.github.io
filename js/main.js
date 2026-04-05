(function() {
    // ======================= 1. 炫酷粒子背景 + 动态连线 =======================
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId = null;
    let mouseX = null, mouseY = null;
    const PARTICLE_COUNT = 85;
    const CONNECT_DIST = 150;
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        initParticles();
    }
    
    function initParticles() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.6,
                vy: (Math.random() - 0.5) * 0.6,
                size: Math.random() * 2.5 + 1,
                color: `hsl(${180 + Math.random() * 60}, 80%, 60%)`
            });
        }
    }
    
    function drawParticles() {
        if (!ctx) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // 绘制连线
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx*dx + dy*dy);
                if (distance < CONNECT_DIST) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(0, 200, 255, ${0.25 * (1 - distance / CONNECT_DIST)})`;
                    ctx.lineWidth = 0.7;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        // 绘制粒子 & 鼠标引力效果
        for (let p of particles) {
            if (mouseX !== null && mouseY !== null) {
                const dx = p.x - mouseX;
                const dy = p.y - mouseY;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 120) {
                    const angle = Math.atan2(dy, dx);
                    const force = (120 - dist) / 500;
                    p.vx += Math.cos(angle) * force;
                    p.vy += Math.sin(angle) * force;
                    let maxSpeed = 1.2;
                    if (p.vx > maxSpeed) p.vx = maxSpeed;
                    if (p.vy > maxSpeed) p.vy = maxSpeed;
                    if (p.vx < -maxSpeed) p.vx = -maxSpeed;
                    if (p.vy < -maxSpeed) p.vy = -maxSpeed;
                }
            }
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;
            
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 6;
            ctx.shadowColor = "#0ff";
            ctx.fill();
        }
        ctx.shadowBlur = 0;
        animationId = requestAnimationFrame(drawParticles);
    }
    
    window.addEventListener('resize', () => {
        resizeCanvas();
    });
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    document.addEventListener('mouseleave', () => {
        mouseX = null;
        mouseY = null;
    });
    
    resizeCanvas();
    drawParticles();
    
    // ======================= 2. 鼠标跟随光晕特效 =======================
    const glow = document.getElementById('glowCursor');
    if (glow) {
        document.addEventListener('mousemove', (e) => {
            if (window.innerWidth > 880) {
                glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
            }
        });
    }
    
    // ======================= 3. Intersection Observer 滚动动画 + 技能条填充 =======================
    const fadeElements = document.querySelectorAll('.fade-up');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2, rootMargin: "0px 0px -40px 0px" });
    
    fadeElements.forEach(el => observer.observe(el));
    
    // 技能进度条填充
    let skillsFilled = false;
    const skillsSection = document.getElementById('skills-section');
    const fillSkillBars = () => {
        if (skillsFilled) return;
        const fills = document.querySelectorAll('.progress-fill');
        fills.forEach(fill => {
            const targetWidth = fill.getAttribute('data-target');
            if (targetWidth) {
                fill.style.width = targetWidth + '%';
            } else {
                const parent = fill.closest('.skill-item');
                if (parent) {
                    const percentSpan = parent.querySelector('.skill-info span:last-child');
                    if (percentSpan) {
                        let val = percentSpan.innerText.replace('%', '');
                        fill.style.width = val + '%';
                    }
                }
            }
        });
        skillsFilled = true;
    };
    
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !skillsFilled) {
                fillSkillBars();
            }
        });
    }, { threshold: 0.3 });
    if (skillsSection) skillObserver.observe(skillsSection);
    
    if (skillsSection) {
        const rect = skillsSection.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100 && !skillsFilled) {
            fillSkillBars();
        }
    }
    
    // ======================= 4. 下滑指示器逻辑 =======================
    const indicator = document.getElementById('scrollIndicator');
    function checkScrollHeight() {
        if (!indicator) return;
        const hasScroll = document.documentElement.scrollHeight > window.innerHeight;
        if (!hasScroll) {
            indicator.classList.add('hide');
            return;
        }
        // 如果滚动超过 80px，隐藏指示器；否则显示
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > 80) {
            indicator.classList.add('hide');
        } else {
            indicator.classList.remove('hide');
        }
    }
    window.addEventListener('scroll', checkScrollHeight);
    window.addEventListener('resize', checkScrollHeight);
    checkScrollHeight(); // 初始化
    
    // ======================= 5. 下载按钮模拟 (生成txt简历并放入file文件夹示意) =======================
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            // 模拟从 file 目录下载 PDF，但由于没有实际pdf，生成一份专业简历文本
            const resumeContent = `陈宇轩 - 全栈开发工程师\n\n联系方式:\n电话: +86 130 1234 5678\n邮箱: yuxuan.chen@dev.me\nGitHub: github.com/yuxuanchen\n\n工作经验:\n1. 星云科技 (资深前端工程师 2022-至今)\n   - 低代码平台核心开发，性能优化提升35%\n2. 深蓝互动 (全栈开发 2019-2022)\n   - Vue3+Node.js 企业级后台，重构权限模块\n\n技能:\nJavaScript/TypeScript, React, Vue, Node.js, Python, CSS3\n\n教育:\n复旦大学 软件工程硕士 (2023-2025)\n南京大学 计算机科学与技术 学士 (2015-2019)\n\n项目精选:\n- Nebula Admin: 动态权限后台\n- Vision Flow: 可视化编辑器\n- AI 面试模拟器: 语音交互AI助手\n\n更多信息请访问在线作品集。`;
            const blob = new Blob([resumeContent], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ChenYuxuan_Resume.txt';   // 实际可替换为 file/resume.pdf
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            const originalText = downloadBtn.innerHTML;
            downloadBtn.innerHTML = '<i class="fas fa-check"></i> 已下载简历';
            setTimeout(() => {
                downloadBtn.innerHTML = originalText;
            }, 1800);
        });
    }
    
    // 控制台个性标语
    console.log("%c⚡ 炫酷简历已加载 | 粒子系统 + 动态下滑指示器 | 欢迎联系 ⚡", "color: #0ff; font-size: 16px; font-weight: bold;");
    
    // 页面可见性优化canvas性能
    let hiddenFlag = false;
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            if (animationId) cancelAnimationFrame(animationId);
            hiddenFlag = true;
        } else {
            if (hiddenFlag) {
                drawParticles();
                hiddenFlag = false;
            }
        }
    });
})();