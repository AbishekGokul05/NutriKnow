# NutriKnow - Food Ingredient Analysis App

This is the frontend for the NutriKnow application, a food ingredient analysis tool that helps users make informed decisions about the products they consume.

## Features

- **Scan Product Ingredients**: Upload images of product ingredient lists for instant analysis
- **Track History**: Keep a record of all products you've scanned
- **User Profile**: Customize your health preferences and dietary restrictions

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the project directory
   ```
   cd health-app
   ```
3. Install dependencies
   ```
   npm install
   ```
   or
   ```
   yarn
   ```

### Development

Start the development server:

```
npm run dev
```
or
```
yarn dev
```

The application will be available at http://localhost:5173/

### Building for Production

```
npm run build
```
or
```
yarn build
```

### Running Tests

```
npm run test
```
or
```
yarn test
```

## Project Structure

- `src/` - Main source code
  - `components/` - Reusable UI components
    - `Navbar.jsx` - Navigation bar component
    - `Scanner.jsx` - Component for scanning and analyzing product ingredients
    - `HistoryDisplay.jsx` - Component for displaying scan history
    - `UserProfile.jsx` - Component for managing user profiles and preferences
  - `App.jsx` - Main application component with routing
  - `main.jsx` - Entry point

## Technologies Used

- React (with Vite)
- React Router for navigation
- Tailwind CSS for styling
- Axios for API requests

## Backend Integration

The application connects to a FastAPI backend for ingredient analysis. Ensure the backend is running at `http://localhost:8000` for full functionality.
