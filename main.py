from app import create_app

# Create the application instance 
app = create_app()

# Run the application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
