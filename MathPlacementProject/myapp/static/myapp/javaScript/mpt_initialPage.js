// Global variables
const categories = ["Algebra", "Calculus", "Geometry", "Trigonometry"];
let currentCategory = null;
let editingId = null;
let selectedQuestionId = null;
let selectedTestQuestionId = null;

// Sample data (in a real app, this would come from a database)
const sampleData = {
    "Algebra": [
        {id: 1, question: "Solve for x: 2x + 3 = 9", correctAnswer: "x = 3"},
        {id: 2, question: "Factor: x² - 9", correctAnswer: "(x+3)(x-3)"},
        {id: 3, question: "Solve the system: x + y = 5, 2x - y = 1", correctAnswer: "x = 2, y = 3"}
    ],
    "Calculus": [
        {id: 1, question: "Find the derivative of f(x) = x³", correctAnswer: "f'(x) = 3x²"},
        {id: 2, question: "Evaluate: ∫(2x + 3)dx", correctAnswer: "x² + 3x + C"}
    ],
    "Geometry": [
        {id: 1, question: "Area of a circle with radius 5", correctAnswer: "25π"},
        {id: 2, question: "Find the perimeter of a rectangle with length 8 and width 6", correctAnswer: "28"}
    ],
    "Trigonometry": [
        {id: 1, question: "sin(π/2) = ?", correctAnswer: "1"},
        {id: 2, question: "cos(0) = ?", correctAnswer: "1"}
    ]
};

// Sample test data
const sampleTestData = {
    "Test1": [
        {id: 1, question: "Solve for x: 2x + 3 = 9", section: "Algebra"},
        {id: 2, question: "Find the derivative of f(x) = x³", section: "Calculus"},
        {id: 3, question: "Find the perimeter of a rectangle with length 8 and width 6", section: "Geometry"}
    ],
    "Test2": [
        {id: 1, question: "Factor: x² - 9", section: "Algebra"},
        {id: 2, question: "Evaluate: ∫(2x + 3)dx", section: "Calculus"}
    ]
};

// DOM Elements - Add/Modify tab
const addModifyBtn = document.getElementById('addModifyBtn');
const makeTestBtn = document.getElementById('makeTestBtn');
const addModifyTab = document.getElementById('addModifyTab');
const makeTestTab = document.getElementById('makeTestTab');
const categoryDropdown = document.getElementById('categoryDropdown');
const emptyLeftPanel = document.getElementById('emptyLeftPanel');
const questionForm = document.getElementById('questionForm');
const emptyTablePanel = document.getElementById('emptyTablePanel');
const questionsTableContainer = document.getElementById('questionsTableContainer');
const categoryTitle = document.getElementById('categoryTitle');
const questionsTable = document.getElementById('questionsTable');

// DOM Elements - Form
const questionText = document.getElementById('questionText');
const answer1Text = document.getElementById('answer1Text');
const answer2Text = document.getElementById('answer2Text');
const answer3Text = document.getElementById('answer3Text');
const answer4Text = document.getElementById('answer4Text');
const clearBtn = document.getElementById('clearBtn');
const addBtn = document.getElementById('addBtn');

// DOM Elements - Make Test tab
const testsTable = document.getElementById('testsTable');
const addTestBtn = document.getElementById('addTestBtn');
const modifyTestBtn = document.getElementById('modifyTestBtn');
const deleteTestBtn = document.getElementById('deleteTestBtn');
const testConfigFrame = document.getElementById('testConfigFrame');
const numQuestionsInput = document.getElementById('numQuestionsInput');
const applyNumBtn = document.getElementById('applyNumBtn');
const sectionFrame = document.getElementById('sectionFrame');
const remainingLabel = document.getElementById('remainingLabel');
const sectionInputs = document.getElementById('sectionInputs');
const generateTestBtn = document.getElementById('generateTestBtn');
const testNameInput = document.getElementById('testNameInput');
const testQuestionsTable = document.getElementById('testQuestionsTable');
const clearTestBtn = document.getElementById('clearTestBtn');
const downloadScriptBtn = document.getElementById('downloadScriptBtn');

// DOM Elements - Context Menus
const tableContextMenu = document.getElementById('tableContextMenu');
const modifyQuestionItem = document.getElementById('modifyQuestionItem');
const deleteQuestionItem = document.getElementById('deleteQuestionItem');
const testQuestionMenu = document.getElementById('testQuestionMenu');
const changeSameSectionItem = document.getElementById('changeSameSectionItem');
const changeDifferentSectionItem = document.getElementById('changeDifferentSectionItem');
const changeManuallyItem = document.getElementById('changeManuallyItem');
const deleteTestQuestionItem = document.getElementById('deleteTestQuestionItem');
const sectionSelectionMenu = document.getElementById('sectionSelectionMenu');

// Tab switching
addModifyBtn.addEventListener('click', () => {
    addModifyBtn.classList.add('active');
    makeTestBtn.classList.remove('active');
    addModifyTab.classList.add('active');
    makeTestTab.classList.remove('active');
});

makeTestBtn.addEventListener('click', () => {
    makeTestBtn.classList.add('active');
    addModifyBtn.classList.remove('active');
    makeTestTab.classList.add('active');
    addModifyTab.classList.remove('active');
});

// Category selection
categoryDropdown.addEventListener('change', () => {
    currentCategory = categoryDropdown.value;
    
    // Show question form and table
    emptyLeftPanel.classList.add('hidden');
    questionForm.classList.remove('hidden');
    emptyTablePanel.classList.add('hidden');
    questionsTableContainer.classList.remove('hidden');
    
    // Update category title
    categoryTitle.textContent = `${currentCategory} Questions`;
    
    // Clear question form
    clearQuestionForm();
    
    // Load questions
    loadQuestions();
});

// Question form handlers
clearBtn.addEventListener('click', clearQuestionForm);

addBtn.addEventListener('click', () => {
    // Get values from the form
    const question = questionText.value.trim();
    const correctAnswer = answer1Text.value.trim();
    const incorrect1 = answer2Text.value.trim();
    const incorrect2 = answer3Text.value.trim();
    const incorrect3 = answer4Text.value.trim();
    
    // Basic validation
    if (!question || !correctAnswer || !incorrect1 || !incorrect2 || !incorrect3) {
        alert("All fields are required");
        return;
    }
    
    if (editingId !== null) {
        // Update existing question
        updateQuestion(editingId, question, correctAnswer);
        alert("Question updated successfully");
    } else {
        // Add new question
        addQuestion(question, correctAnswer);
        alert("Question added successfully");
    }
    
    // Clear the form
    clearQuestionForm();
});

// Table context menu
document.addEventListener('click', () => {
    tableContextMenu.style.display = 'none';
    testQuestionMenu.style.display = 'none';
    sectionSelectionMenu.style.display = 'none';
});

questionsTable.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    
    // Find the closest row
    const row = e.target.closest('tr');
    if (row && row.parentNode.tagName === 'TBODY') {
        // Select the row
        const rows = questionsTable.querySelectorAll('tbody tr');
        rows.forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
        selectedQuestionId = row.dataset.id;
        
        // Show context menu
        tableContextMenu.style.display = 'block';
        tableContextMenu.style.left = `${e.pageX}px`;
        tableContextMenu.style.top = `${e.pageY}px`;
    }
});

modifyQuestionItem.addEventListener('click', () => {
    modifyQuestion(selectedQuestionId);
});

deleteQuestionItem.addEventListener('click', () => {
    if (confirm("Are you sure you want to delete this question?")) {
        deleteQuestion(selectedQuestionId);
        alert("Question deleted successfully");
    }
});

// Test Management
addTestBtn.addEventListener('click', () => {
    testConfigFrame.classList.remove('hidden');
    clearTest();
    numQuestionsInput.focus();
});

applyNumBtn.addEventListener('click', () => {
    const numQuestions = parseInt(numQuestionsInput.value);
    if (isNaN(numQuestions) || numQuestions <= 0) {
        alert("Please enter a valid number of questions");
        return;
    }
    
    // Create section allocation inputs
    createSectionInputs(numQuestions);
});

generateTestBtn.addEventListener('click', generateTest);

modifyTestBtn.addEventListener('click', () => {
    const selectedRow = testsTable.querySelector('tbody tr.selected');
    if (!selectedRow) {
        alert("Please select a test to modify");
        return;
    }
    
    const testName = selectedRow.cells[0].textContent;
    modifyTest(testName);
});

deleteTestBtn.addEventListener('click', () => {
    const selectedRow = testsTable.querySelector('tbody tr.selected');
    if (!selectedRow) {
        alert("Please select a test to delete");
        return;
    }
    
    if (confirm("Are you sure you want to delete this test?")) {
        selectedRow.remove();
        clearTest();
    }
});

clearTestBtn.addEventListener('click', clearTest);

downloadScriptBtn.addEventListener('click', () => {
    alert("This would generate and download a script for the test");
});

// Test table context menu
testQuestionsTable.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    
    // Find the closest row
    const row = e.target.closest('tr');
    if (row && row.parentNode.tagName === 'TBODY') {
        // Select the row
        const rows = testQuestionsTable.querySelectorAll('tbody tr');
        rows.forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
        selectedTestQuestionId = row.dataset.id;
        
        // Show context menu
        testQuestionMenu.style.display = 'block';
        testQuestionMenu.style.left = `${e.pageX}px`;
        testQuestionMenu.style.top = `${e.pageY}px`;
    }
});

changeSameSectionItem.addEventListener('click', () => {
    changeWithSameSection();
});

changeDifferentSectionItem.addEventListener('click', (e) => {
    if (!selectedTestQuestionId) return;
    
    // Show section selection menu
    sectionSelectionMenu.style.display = 'block';
    sectionSelectionMenu.style.left = `${e.pageX}px`;
    sectionSelectionMenu.style.top = `${e.pageY}px`;
    
    e.stopPropagation();
});

// Section selection menu
document.querySelectorAll('#sectionSelectionMenu .context-menu-item').forEach(item => {
    item.addEventListener('click', (e) => {
        const newSection = e.target.dataset.section;
        changeWithDifferentSection(newSection);
    });
});

changeManuallyItem.addEventListener('click', () => {
    alert("This would open a dialog to select a specific question from the database");
});

deleteTestQuestionItem.addEventListener('click', () => {
    deleteTestQuestion();
});

// Make tests table rows selectable
testsTable.addEventListener('click', (e) => {
    const row = e.target.closest('tr');
    if (row && row.parentNode.tagName === 'TBODY') {
        // Select the row
        const rows = testsTable.querySelectorAll('tbody tr');
        rows.forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
    }
});

// Function to clear question form
function clearQuestionForm() {
    questionText.value = '';
    answer1Text.value = '';
    answer2Text.value = '';
    answer3Text.value = '';
    answer4Text.value = '';
    
    editingId = null;
    addBtn.textContent = 'Add Question';
}

// Function to load questions for the selected category
function loadQuestions() {
    // Clear existing rows
    const tbody = questionsTable.querySelector('tbody');
    tbody.innerHTML = '';
    
    // Add questions
    if (sampleData[currentCategory]) {
        sampleData[currentCategory].forEach(item => {
            const row = document.createElement('tr');
            row.dataset.id = item.id;
            
            const idCell = document.createElement('td');
            idCell.textContent = item.id;
            
            const questionCell = document.createElement('td');
            questionCell.textContent = item.question;
            
            const answerCell = document.createElement('td');
            answerCell.textContent = item.correctAnswer;
            
            row.appendChild(idCell);
            row.appendChild(questionCell);
            row.appendChild(answerCell);
            
            tbody.appendChild(row);
        });
    }
}

// Function to add a new question
function addQuestion(question, correctAnswer) {
    // Generate a simple ID
    const newId = sampleData[currentCategory] ? sampleData[currentCategory].length + 1 : 1;
    
    // Add to sample data
    if (!sampleData[currentCategory]) {
        sampleData[currentCategory] = [];
    }
    
    sampleData[currentCategory].push({
        id: newId,
        question: question,
        correctAnswer: correctAnswer
    });
    
    // Add to table
    const tbody = questionsTable.querySelector('tbody');
    const row = document.createElement('tr');
    row.dataset.id = newId;
    
    const idCell = document.createElement('td');
    idCell.textContent = newId;
    
    const questionCell = document.createElement('td');
    questionCell.textContent = question;
    
    const answerCell = document.createElement('td');
    answerCell.textContent = correctAnswer;
    
    row.appendChild(idCell);
    row.appendChild(questionCell);
    row.appendChild(answerCell);
    
    tbody.appendChild(row);
}

// Function to update an existing question
function updateQuestion(id, question, correctAnswer) {
    // Update in sample data
    const questionData = sampleData[currentCategory].find(q => q.id == id);
    if (questionData) {
        questionData.question = question;
        questionData.correctAnswer = correctAnswer;
    }
    
    // Update in table
    const row = questionsTable.querySelector(`tbody tr[data-id="${id}"]`);
    if (row) {
        row.cells[1].textContent = question;
        row.cells[2].textContent = correctAnswer;
    }
}

// Function to modify a question
function modifyQuestion(id) {
    // Find the question data
    const questionData = sampleData[currentCategory].find(q => q.id == id);
    if (!questionData) return;
    
    // Fill the form
    questionText.value = questionData.question;
    answer1Text.value = questionData.correctAnswer;
    answer2Text.value = "Incorrect answer 1";
    answer3Text.value = "Incorrect answer 2";
    answer4Text.value = "Incorrect answer 3";
    
    // Set editing state
    editingId = id;
    addBtn.textContent = 'Update Question';
}

// Function to delete a question
function deleteQuestion(id) {
    // Remove from sample data
    const index = sampleData[currentCategory].findIndex(q => q.id == id);
    if (index !== -1) {
        sampleData[currentCategory].splice(index, 1);
    }
    
    // Remove from table
    const row = questionsTable.querySelector(`tbody tr[data-id="${id}"]`);
    if (row) {
        row.remove();
    }
}

// Function to create section inputs
// Function to create section inputs
function createSectionInputs(totalQuestions) {
// Clear existing inputs
sectionInputs.innerHTML = '';

// Create input for each category
let total = 0;

categories.forEach(category => {
const div = document.createElement('div');
div.className = 'form-row mb-10';

const label = document.createElement('label');
label.textContent = `${category}:`;

const input = document.createElement('input');
input.type = 'number';
input.className = 'section-input';
input.min = '0';
input.max = totalQuestions;
input.value = '0';
input.dataset.category = category;

input.addEventListener('change', () => {
    updateRemaining();
});

div.appendChild(label);
div.appendChild(input);

sectionInputs.appendChild(div);
});

// Show section frame
sectionFrame.classList.remove('hidden');

// Initialize remaining count
remainingLabel.textContent = `Remaining: ${totalQuestions}`;

// Update function for remaining count
function updateRemaining() {
let allocated = 0;
document.querySelectorAll('.section-input').forEach(input => {
    allocated += parseInt(input.value) || 0;
});

const remaining = totalQuestions - allocated;
remainingLabel.textContent = `Remaining: ${remaining}`;

// Enable/disable generate button
generateTestBtn.disabled = remaining !== 0;
}
}

// Function to generate a test
function generateTest() {
// Get test name
const testName = testNameInput.value.trim();
if (!testName) {
alert("Please enter a test name");
return;
}

// Get section allocations
const allocations = {};
let totalAllocated = 0;

document.querySelectorAll('.section-input').forEach(input => {
const category = input.dataset.category;
const count = parseInt(input.value) || 0;
allocations[category] = count;
totalAllocated += count;
});

// Validate total
const totalQuestions = parseInt(numQuestionsInput.value);
if (totalAllocated !== totalQuestions) {
alert("The number of allocated questions doesn't match the total");
return;
}

// Clear existing test questions
const tbody = testQuestionsTable.querySelector('tbody');
tbody.innerHTML = '';

// Generate questions for each category
let questionNumber = 1;

for (const category in allocations) {
const count = allocations[category];
if (count > 0) {
    // Get available questions for this category
    const availableQuestions = sampleData[category] || [];
    
    // Check if we have enough questions
    if (availableQuestions.length < count) {
        alert(`Not enough questions in ${category}. Need ${count}, but only have ${availableQuestions.length}`);
        return;
    }
    
    // Randomly select questions
    const selectedQuestions = getRandomQuestions(availableQuestions, count);
    
    // Add to test
    selectedQuestions.forEach(q => {
        addTestQuestion(questionNumber++, q.question, category);
    });
}
}

// Add to test list if it doesn't exist
const existingTest = Array.from(testsTable.querySelectorAll('tbody tr'))
.find(row => row.cells[0].textContent === testName);

if (!existingTest) {
const row = document.createElement('tr');
const cell = document.createElement('td');
cell.textContent = testName;
row.appendChild(cell);
testsTable.querySelector('tbody').appendChild(row);
}

// Save to sample test data
sampleTestData[testName] = Array.from(tbody.querySelectorAll('tr')).map(row => ({
id: parseInt(row.dataset.id),
question: row.cells[1].textContent,
section: row.cells[2].textContent
}));

// Alert success
alert(`Test "${testName}" generated successfully with ${totalQuestions} questions`);
}

// Function to get random questions from a list
function getRandomQuestions(questions, count) {
// Create a copy of the questions array
const available = [...questions];
const selected = [];

// Select random questions
for (let i = 0; i < count; i++) {
const randomIndex = Math.floor(Math.random() * available.length);
selected.push(available[randomIndex]);
available.splice(randomIndex, 1);
}

return selected;
}

// Function to add a question to the test table
function addTestQuestion(number, question, section) {
const tbody = testQuestionsTable.querySelector('tbody');
const row = document.createElement('tr');
row.dataset.id = number;

const numberCell = document.createElement('td');
numberCell.textContent = number;

const questionCell = document.createElement('td');
questionCell.textContent = question;

const sectionCell = document.createElement('td');
sectionCell.textContent = section;

row.appendChild(numberCell);
row.appendChild(questionCell);
row.appendChild(sectionCell);

tbody.appendChild(row);
}

// Function to modify an existing test
function modifyTest(testName) {
// Load test data
const testData = sampleTestData[testName];
if (!testData) return;

// Set test name
testNameInput.value = testName;

// Clear existing test questions
const tbody = testQuestionsTable.querySelector('tbody');
tbody.innerHTML = '';

// Add questions to the table
testData.forEach(item => {
addTestQuestion(item.id, item.question, item.section);
});

// Show test config panel
testConfigFrame.classList.remove('hidden');
numQuestionsInput.value = testData.length;

// Set up section inputs
createSectionInputs(testData.length);

// Count questions by section
const sectionCounts = {};
testData.forEach(item => {
sectionCounts[item.section] = (sectionCounts[item.section] || 0) + 1;
});

// Set section input values
document.querySelectorAll('.section-input').forEach(input => {
const category = input.dataset.category;
input.value = sectionCounts[category] || 0;
});
}

// Function to clear the test
function clearTest() {
testNameInput.value = "New Test";
testQuestionsTable.querySelector('tbody').innerHTML = '';
numQuestionsInput.value = '';
sectionFrame.classList.add('hidden');
}

// Function to change a test question with one from the same section
function changeWithSameSection() {
if (!selectedTestQuestionId) return;

// Find the selected row
const row = testQuestionsTable.querySelector(`tbody tr[data-id="${selectedTestQuestionId}"]`);
if (!row) return;

// Get the section
const section = row.cells[2].textContent;

// Get available questions from this section
const availableQuestions = sampleData[section] || [];
if (availableQuestions.length === 0) {
alert(`No questions available in ${section}`);
return;
}

// Get current test questions
const currentTestQuestions = Array.from(testQuestionsTable.querySelectorAll('tbody tr'))
.map(row => row.cells[1].textContent);

// Filter out questions already in the test
const unusedQuestions = availableQuestions.filter(q => 
!currentTestQuestions.includes(q.question)
);

if (unusedQuestions.length === 0) {
alert(`All ${section} questions are already in the test`);
return;
}

// Select a random question
const randomIndex = Math.floor(Math.random() * unusedQuestions.length);
const newQuestion = unusedQuestions[randomIndex];

// Update the row
row.cells[1].textContent = newQuestion.question;

// Update in sample test data
const testName = testNameInput.value.trim();
if (sampleTestData[testName]) {
const questionIndex = sampleTestData[testName].findIndex(q => q.id == selectedTestQuestionId);
if (questionIndex !== -1) {
    sampleTestData[testName][questionIndex].question = newQuestion.question;
}
}
}

// Function to change a test question with one from a different section
function changeWithDifferentSection(newSection) {
if (!selectedTestQuestionId || !newSection) return;

// Find the selected row
const row = testQuestionsTable.querySelector(`tbody tr[data-id="${selectedTestQuestionId}"]`);
if (!row) return;

// Get available questions from the new section
const availableQuestions = sampleData[newSection] || [];
if (availableQuestions.length === 0) {
alert(`No questions available in ${newSection}`);
return;
}

// Get current test questions
const currentTestQuestions = Array.from(testQuestionsTable.querySelectorAll('tbody tr'))
.map(row => row.cells[1].textContent);

// Filter out questions already in the test
const unusedQuestions = availableQuestions.filter(q => 
!currentTestQuestions.includes(q.question)
);

if (unusedQuestions.length === 0) {
alert(`All ${newSection} questions are already in the test`);
return;
}

// Select a random question
const randomIndex = Math.floor(Math.random() * unusedQuestions.length);
const newQuestion = unusedQuestions[randomIndex];

// Update the row
row.cells[1].textContent = newQuestion.question;
row.cells[2].textContent = newSection;

// Update in sample test data
const testName = testNameInput.value.trim();
if (sampleTestData[testName]) {
const questionIndex = sampleTestData[testName].findIndex(q => q.id == selectedTestQuestionId);
if (questionIndex !== -1) {
    sampleTestData[testName][questionIndex].question = newQuestion.question;
    sampleTestData[testName][questionIndex].section = newSection;
}
}
}

// Function to delete a test question
function deleteTestQuestion() {
if (!selectedTestQuestionId) return;

// Find the selected row
const row = testQuestionsTable.querySelector(`tbody tr[data-id="${selectedTestQuestionId}"]`);
if (!row) return;

// Remove the row
row.remove();

// Update in sample test data
const testName = testNameInput.value.trim();
if (sampleTestData[testName]) {
const questionIndex = sampleTestData[testName].findIndex(q => q.id == selectedTestQuestionId);
if (questionIndex !== -1) {
    sampleTestData[testName].splice(questionIndex, 1);
}
}

// Renumber questions
const rows = testQuestionsTable.querySelectorAll('tbody tr');
rows.forEach((row, index) => {
const number = index + 1;
row.dataset.id = number;
row.cells[0].textContent = number;

// Update in sample test data
if (sampleTestData[testName] && sampleTestData[testName][index]) {
    sampleTestData[testName][index].id = number;
}
});
}

// Generate a test script (for download)
function generateTestScript() {
const testName = testNameInput.value.trim();
if (!testName) {
alert("Please enter a test name");
return;
}

// Get test questions
const testQuestions = Array.from(testQuestionsTable.querySelectorAll('tbody tr')).map(row => ({
number: parseInt(row.cells[0].textContent),
question: row.cells[1].textContent,
section: row.cells[2].textContent
}));

if (testQuestions.length === 0) {
alert("No questions in the test");
return;
}

// Create test script
let script = `# ${testName}\n\n`;

// Add questions
testQuestions.forEach(q => {
script += `## Question ${q.number} (${q.section})\n`;
script += `${q.question}\n\n`;
});

// In a real application, this would trigger a download
console.log(script);
alert("Test script generated (simulated download)");
}

// Initialize downloadScriptBtn click handler
downloadScriptBtn.addEventListener('click', generateTestScript);

// Initialize the application
function initApp() {
// Add test list click handler
testsTable.addEventListener('click', (e) => {
const row = e.target.closest('tr');
if (row && row.parentNode.tagName === 'TBODY') {
    // Select the row
    const rows = testsTable.querySelectorAll('tbody tr');
    rows.forEach(r => r.classList.remove('selected'));
    row.classList.add('selected');
}
});

// Double-click on test to modify
testsTable.addEventListener('dblclick', (e) => {
const row = e.target.closest('tr');
if (row && row.parentNode.tagName === 'TBODY') {
    const testName = row.cells[0].textContent;
    modifyTest(testName);
}
});

// Double-click on question to modify
questionsTable.addEventListener('dblclick', (e) => {
const row = e.target.closest('tr');
if (row && row.parentNode.tagName === 'TBODY') {
    const id = row.dataset.id;
    modifyQuestion(id);
}
});
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initApp);