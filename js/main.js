(function() {
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) { console.error('Canvas context not available'); return; }
    
    let particles = [];
    let animationId = null;
    let mouseX = null, mouseY = null;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        initParticles();
    }

    function initParticles() {
        particles = [];
        const count = Math.floor((canvas.width * canvas.height) / 8000);
        for (let i = 0; i < count; i++) {
            const isLarge = Math.random() > 0.92;
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 1,
                vy: (Math.random() - 0.5) * 1,
                size: isLarge ? Math.random() * 2.5 + 2 : Math.random() * 1.5 + 0.8,
                color: isLarge ? '#ffffff' : `hsl(${170 + Math.random() * 50}, 80%, 60%)`,
                alpha: isLarge ? 0.95 : Math.random() * 0.5 + 0.4,
                pulse: Math.random() * Math.PI * 2,
                pulseSpeed: Math.random() * 0.04 + 0.015,
                isLarge: isLarge
            });
        }
    }

    function drawParticles() {
        ctx.fillStyle = '#050810';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 连线
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const p1 = particles[i];
                const p2 = particles[j];
                const dist = Math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2);
                if (dist < 100) {
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(0, 255, 255, ${(1 - dist / 100) * 0.15})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }

        // 粒子
        for (let p of particles) {
            p.pulse += p.pulseSpeed;
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;

            let finalX = p.x, finalY = p.y;
            if (mouseX !== null && mouseY !== null) {
                const dx = p.x - mouseX;
                const dy = p.y - mouseY;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 80) {
                    const force = (80 - dist) / 80;
                    const angle = Math.atan2(dy, dx);
                    finalX = p.x + Math.cos(angle) * force * 25;
                    finalY = p.y + Math.sin(angle) * force * 25;
                }
            }

            const size = p.size * (1 + Math.sin(p.pulse) * 0.25);

            if (p.isLarge) {
                ctx.beginPath();
                ctx.arc(finalX, finalY, size * 2, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(0, 255, 255, 0.12)';
                ctx.fill();
            }

            ctx.beginPath();
            ctx.arc(finalX, finalY, size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.alpha;
            ctx.fill();
            ctx.globalAlpha = 1;
        }

        animationId = requestAnimationFrame(drawParticles);
    }

    window.addEventListener('resize', resizeCanvas);
    document.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });
    document.addEventListener('mouseleave', () => { mouseX = null; mouseY = null; });

    resizeCanvas();
    drawParticles();

    // 鼠标光晕
    const glow = document.getElementById('glowCursor');
    if (glow) {
        document.addEventListener('mousemove', e => {
            if (window.innerWidth > 900) {
                glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
            }
        });
    }

    // 滚动动画
    document.querySelectorAll('.fade-up').forEach(el => {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        observer.observe(el);
    });

    // 技能条
    const skillsSection = document.getElementById('skills-section');
    if (skillsSection) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    document.querySelectorAll('.progress-fill').forEach(fill => {
                        const target = fill.dataset.target;
                        if (target) fill.style.width = target + '%';
                    });
                    observer.unobserve(skillsSection);
                }
            });
        }, { threshold: 0.3 });
        observer.observe(skillsSection);
    }

    // 下滑指示器
    const indicator = document.getElementById('scrollIndicator');
    function checkScroll() {
        if (!indicator) return;
        if (document.documentElement.scrollHeight <= window.innerHeight) {
            indicator.classList.add('hide');
            return;
        }
        const nearBottom = (window.scrollY + window.innerHeight) >= (document.documentElement.scrollHeight - 100);
        indicator.classList.toggle('hide', nearBottom);
    }
    window.addEventListener('scroll', checkScroll);
    window.addEventListener('resize', checkScroll);
    checkScroll();

    // 下载按钮
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const content = '陈宇轩 - 全栈开发工程师\n\n联系方式:\n- 电话: +86 130 1234 5678\n- 邮箱: yuxuan.chen@dev.me\n\n工作经历:\n- 星云科技: 资深前端工程师 (2022-至今)\n- 深蓝互动: 全栈开发工程师 (2019-2022)\n\n技能: JavaScript, React, Vue, Node.js\n\n教育: 复旦大学 软件工程硕士 (在读)';
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '陈宇轩_简历.txt';
            a.click();
            URL.revokeObjectURL(url);
            downloadBtn.innerHTML = '<i class="fas fa-check"></i> 已下载';
            setTimeout(() => downloadBtn.innerHTML = '<i class="fas fa-download"></i> 下载简历', 1500);
        });
    }

    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            if (animationId) cancelAnimationFrame(animationId);
        } else {
            drawParticles();
        }
    });
})();