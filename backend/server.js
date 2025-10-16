const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const port = 8000;

app.use(cors());
app.use(express.json());

mongoose.connect('mongodb://localhost:27017/testcases', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const testCaseSchema = new mongoose.Schema({
  name: String,
  history: [String],
});

const TestCase = mongoose.model('TestCase', testCaseSchema);

app.get('/testcases', async (req, res) => {
  const testCases = await TestCase.find();
  res.json(testCases);
});

app.post('/testcases', async (req, res) => {
  const newTestCase = new TestCase(req.body);
  await newTestCase.save();
  res.json(newTestCase);
});

app.put('/testcases/:id', async (req, res) => {
  const updatedTestCase = await TestCase.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(updatedTestCase);
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});