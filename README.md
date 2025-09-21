# LaTeX Files Web Application

This application is a comprehensive web-based platform for managing, compiling, and sharing LaTeX documents. It is specifically designed for diploma theses and academic papers according to Ukrainian higher education standards. It was developed as part of my own diploma thesis.

## 🌐 Live Web Application

**🚀 Access the platform:** [https://latexfiles-latest.onrender.com/](https://latexfiles-latest.onrender.com/)

The web application provides a complete LaTeX document management system with file upload, compilation, and download capabilities.

## 📋 About the Application

This is a full-stack web application that serves as an online LaTeX document management and compilation platform. It enables users to:

- Upload and manage LaTeX files
- Compile LaTeX documents to PDF online
- Share and collaborate on academic documents  
- Download both source files and compiled PDFs
- Access a repository of LaTeX templates and documents

## 📸 Screenshots
| Home | Document page (for author) |
| ------- | --- |
| <img width="500" alt="image" src="https://github.com/user-attachments/assets/e73fd522-1c6f-4663-8316-6b31be5fee86" />| <img width="500" alt="image" src="https://github.com/user-attachments/assets/be2c2842-9ac6-4a37-97ee-66c9e6b4e671" /> |

| Update Page & Version change | Comments section |
| ------- | --- |
| <img width="1200" alt="image" src="https://github.com/user-attachments/assets/b937351d-3d43-4232-b43b-81390939d21c" />| <img width="500" alt="image" src="https://github.com/user-attachments/assets/de6eb1ec-2e48-4dde-9d54-3da1fec8281c" /> <img width="636" height="188" alt="image" src="https://github.com/user-attachments/assets/1d8ef9a6-db45-40bc-ac84-4387a6d2c778" /> |

| User Profile |
| ------- |
| <img width="1200" alt="image" src="https://github.com/user-attachments/assets/c41b7f0d-6ca6-433e-8082-41bd9b9debe5" /> |


## 🏗️ Application Architecture

### Backend Features
- **File Management System**: Upload, store, and organize LaTeX files
- **LaTeX Compilation Engine**: Server-side PDF generation from LaTeX source
- **User Management**: Multi-user support with file ownership tracking
- **Database Integration**: Persistent storage of documents and metadata

### Frontend Features  
- **File Upload Interface**: Browse file upload
- **Document Library**: Browse and search uploaded documents
- **Download Manager**: Direct download of TEX files and compiled PDFs
- **User Dashboard**: Personal document management interface

## 🛠️ Technology Stack

### Core Technologies
- **Backend Framework**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3
- **LaTeX Engine**: TexLive distribution for document compilation

### DevOps & Deployment
- **Containerization**: Docker for application packaging
- **Container Registry**: Docker Hub for image distribution
- **Cloud Platform**: Render for production deployment


## 🛠️ Application Features

### Document Management
- ✅ **File Upload**: Support for .tex
- ✅ **Archive Handling**: Upload and extract .tar.gz and .zip archives
- ✅ **Version Control**: Track document versions and changes
- ✅ **Online Compilation**: Server-side LaTeX to PDF conversion

### User Experience
- ✅ **Intuitive Interface**: Clean, user-friendly web design
- ✅ **Instant Downloads**: Quick access to source files and PDFs
- ✅ **Document Preview**: Online PDF viewing capabilities
- ✅ **Search Functionality**: Find documents by name
- ✅ **Comments Section**: Leave comments in documents comment section

### Academic Focus
- ✅ **Thesis Templates**: Pre-configured templates for Ukrainian universities
- ✅ **Standards Compliance**: DSTU and institutional formatting requirements
- ✅ **Bibliography Support**: BibTeX integration and citation management
- ✅ **Multi-language**: Support for Ukrainian, English, and other languages

## 🚀 Using the Web Application

### For Document Upload:
1. Visit [https://latexfiles-latest.onrender.com/](https://latexfiles-latest.onrender.com/)
2. Login into service
3. Click upload
4. Supported formats: `.tex`, `.tar.gz`, `.zip`
5. Files are automatically processed and made available

### For Document Access:
1. Browse the document library on the main page
2. Click download icons to get:
   - 📄 **TEX files**: Source LaTeX documents
   - 📋 **PDF files**: Compiled output documents
3. Documents are organized by upload date

## 🐳 Deployment

The application is containerized using Docker and deployed on Render platform via Docker Hub registry.

## 🌟 Key Advantages

### Over Traditional LaTeX Workflows:
- **No Local Installation**: Use LaTeX without installing TeX distribution
- **Version Management**: Automatic backup and version tracking

## 📚 Supported Document Types

- **Diploma Theses**: Bachelor's and Master's degree papers
- **Research Papers**: Academic articles and conference papers
- **Course Projects**: Semester and course-related assignments
- **Technical Documentation**: Reports, manuals, and specifications
- **Academic Presentations**: Beamer slides and presentations

## 📄 License & Terms

This web application was made as a part of diploma thesis.

---

**Deployment**: 🐳 Dockerized and deployed on Render via Docker Hub  
**Container Registry**: Available on Docker Hub for easy deployment
