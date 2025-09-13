# Synthetic Data Generator API

A FastAPI-based service for generating synthetic datasets using the GReaT (Generating Realistic Tabular Data) model.

## Features

- **File Upload**: Upload CSV datasets for synthetic data generation
- **Synthetic Data Generation**: Generate realistic synthetic data using GReaT model
- **Quality Metrics**: Calculate privacy and quality metrics for generated data
- **File Download**: Download generated synthetic datasets
- **Session Management**: Track and manage user sessions
- **Automatic Cleanup**: Clean up temporary files automatically

## Installation

1. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Linux/Mac:
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

```bash
python run_server.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. Upload Dataset
```http
POST /upload
Content-Type: multipart/form-data

Form data:
- file: CSV file to upload
```

**Response**:
```json
{
  "session_id": "uuid-string",
  "filename": "dataset.csv",
  "message": "File uploaded successfully",
  "file_path": "/path/to/uploaded/file"
}
```

#### 2. Generate Synthetic Data
```http
POST /generate
Content-Type: application/json

{
  "session_id": "uuid-string",
  "n_samples": 100,
  "epochs": 30,
  "batch_size": 32
}
```

**Response**:
```json
{
  "session_id": "uuid-string",
  "synthetic_data_path": "/path/to/synthetic/data",
  "n_samples": 100,
  "quality_metrics": {
    "exact_match_count": 0,
    "nearest_neighbor_distance": 10.8720,
    "membership_inference_risk": 0.0000,
    "additional_metrics": {...}
  },
  "message": "Synthetic data generated successfully"
}
```

#### 3. Download Synthetic Data
```http
GET /download/{session_id}
```

Returns the synthetic dataset as a CSV file.

#### 4. Cleanup Session
```http
DELETE /cleanup/{session_id}
```

Cleans up all files associated with a session.

### Example Usage with curl

1. **Upload a dataset**:
   ```bash
   curl -X POST "http://localhost:8000/upload" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@your_dataset.csv"
   ```

2. **Generate synthetic data**:
   ```bash
   curl -X POST "http://localhost:8000/generate" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{
          "session_id": "your-session-id",
          "n_samples": 100,
          "epochs": 30,
          "batch_size": 32
        }'
   ```

3. **Download synthetic data**:
   ```bash
   curl -X GET "http://localhost:8000/download/your-session-id" \
        --output synthetic_data.csv
   ```

## Configuration

### Environment Variables

- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: "true")

### Model Parameters

- `n_samples`: Number of synthetic samples to generate (1-10000)
- `epochs`: Training epochs (1-100)
- `batch_size`: Training batch size (1-128)

## Quality Metrics

The API calculates several quality metrics:

1. **Exact Match Count**: Number of identical rows between real and synthetic data
2. **Nearest Neighbor Distance**: Average distance from synthetic records to closest real record
3. **Membership Inference Risk**: Risk of membership inference attack
4. **Additional Metrics**: Data shape, columns, and data types

## File Management

- Uploaded files are stored temporarily in the system temp directory
- Files are automatically cleaned up after 24 hours
- Each session gets a unique UUID for file organization
- Manual cleanup is available via the cleanup endpoint

## Error Handling

The API includes comprehensive error handling for:
- Invalid file formats
- Missing sessions
- Model training failures
- File system errors
- Validation errors

## Development

### Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application
├── models/
│   ├── __init__.py
│   └── synthetic_generator.py  # GReaT model wrapper
├── schemas/
│   ├── __init__.py
│   ├── request_schemas.py  # Request models
│   └── response_schemas.py # Response models
└── services/
    ├── __init__.py
    └── file_service.py     # File handling service
```

### Running in Development

```bash
# With auto-reload
python run_server.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Requirements

- Python 3.8+
- FastAPI
- GReaT (be-great)
- Pandas
- NumPy
- Scikit-learn
- PyTorch
- And other dependencies listed in `requirements.txt`

## License

This project is for educational and research purposes.
