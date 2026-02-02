// Simple test to validate the JSX structure by checking bracket balance
const fs = require('fs');

const content = fs.readFileSync('frontend/src/components/ChatWidget.tsx', 'utf8');

// Count various types of brackets
let parenCount = 0;
let braceCount = 0;
let bracketCount = 0;

for (let i = 0; i < content.length; i++) {
  const char = content[i];
  switch (char) {
    case '(':
      parenCount++;
      break;
    case ')':
      parenCount--;
      break;
    case '{':
      braceCount++;
      break;
    case '}':
      braceCount--;
      break;
    case '[':
      bracketCount++;
      break;
    case ']':
      bracketCount--;
      break;
  }
}

console.log('Parentheses balance:', parenCount);
console.log('Braces balance:', braceCount);
console.log('Brackets balance:', bracketCount);

if (parenCount === 0 && braceCount === 0 && bracketCount === 0) {
  console.log('✅ All brackets are balanced!');
} else {
  console.log('❌ Some brackets are unbalanced!');
}