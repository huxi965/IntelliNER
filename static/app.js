// 全局变量
let entityTypes = {};

// DOM元素
const inputText = document.getElementById('inputText');
const exampleSelect = document.getElementById('exampleSelect');
const predictBtn = document.getElementById('predictBtn');
const clearBtn = document.getElementById('clearBtn');
const resultSection = document.getElementById('resultSection');
const highlightedText = document.getElementById('highlightedText');
const entitiesTableBody = document.getElementById('entitiesTableBody');
const processingTime = document.getElementById('processingTime');
const loadingOverlay = document.getElementById('loadingOverlay');

// 初始化
async function init() {
    await loadEntityTypes();
    await loadExamples();
}

// 加载实体类型配置
async function loadEntityTypes() {
    try {
        const response = await fetch('/api/ner/entity-types');
        entityTypes = await response.json();
    } catch (error) {
        console.error('加载实体类型失败:', error);
    }
}

// 加载示例文本
async function loadExamples() {
    try {
        const response = await fetch('/api/ner/examples');
        const examples = await response.json();

        examples.forEach((example, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = example.title;
            option.dataset.text = example.text;
            exampleSelect.appendChild(option);
        });
    } catch (error) {
        console.error('加载示例失败:', error);
    }
}

// 选择示例文本
exampleSelect.addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    if (selectedOption.dataset.text) {
        inputText.value = selectedOption.dataset.text;
    }
});

// 执行识别
predictBtn.addEventListener('click', async () => {
    const text = inputText.value.trim();

    if (!text) {
        alert('请输入文本！');
        return;
    }

    // 显示加载状态
    loadingOverlay.style.display = 'flex';
    resultSection.style.display = 'none';

    try {
        const response = await fetch('/api/ner/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error('识别失败');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        alert('识别出错：' + error.message);
        console.error(error);
    } finally {
        loadingOverlay.style.display = 'none';
    }
});

// 显示结果
function displayResults(data) {
    // 显示处理时间
    processingTime.textContent = `⚡ 耗时: ${data.processing_time.toFixed(3)}秒`;

    // 生成高亮文本
    const highlightedHtml = generateHighlightedText(data.text, data.entities);
    highlightedText.innerHTML = highlightedHtml;

    // 生成实体表格
    generateEntitiesTable(data.entities);

    // 显示结果区
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// 生成高亮文本
function generateHighlightedText(text, entities) {
    if (entities.length === 0) {
        return `<p style="color: #6b7280;">未识别到任何实体</p>`;
    }

    // 按位置排序
    const sortedEntities = [...entities].sort((a, b) => a.start - b.start);

    let result = '';
    let lastIndex = 0;

    sortedEntities.forEach(entity => {
        // 添加实体之前的文本
        result += escapeHtml(text.substring(lastIndex, entity.start));

        // 添加高亮实体
        const entityClass = `entity-highlight entity-${entity.type}`;
        const entityLabel = entityTypes[entity.type]?.label || entity.type;
        result += `<span class="${entityClass}" title="${entityLabel} (${(entity.confidence * 100).toFixed(1)}%)">${escapeHtml(entity.text)}</span>`;

        lastIndex = entity.end;
    });

    // 添加剩余文本
    result += escapeHtml(text.substring(lastIndex));

    return result;
}

// 生成实体表格
function generateEntitiesTable(entities) {
    entitiesTableBody.innerHTML = '';

    if (entities.length === 0) {
        entitiesTableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #6b7280;">暂无数据</td></tr>';
        return;
    }

    entities.forEach((entity, index) => {
        const row = document.createElement('tr');

        const typeConfig = entityTypes[entity.type] || { label: entity.type, color: '#6b7280' };

        row.innerHTML = `
            <td><strong>${escapeHtml(entity.text)}</strong></td>
            <td>
                <span class="entity-badge" style="background-color: ${typeConfig.color}20; color: ${typeConfig.color};">
                    ${typeConfig.label}
                </span>
            </td>
            <td>${entity.start} - ${entity.end}</td>
            <td>${(entity.confidence * 100).toFixed(1)}%</td>
        `;

        entitiesTableBody.appendChild(row);
    });
}

// 清空
clearBtn.addEventListener('click', () => {
    inputText.value = '';
    exampleSelect.value = '';
    resultSection.style.display = 'none';
});

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);