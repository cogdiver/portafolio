#!/bin/bash

# --------------------------------------------------------------------------------
# Script to Create a New Template Structure
#
# This script guides the user to create a directory structure for a new
# Cookiecutter template within the project. It includes user prompts to define
# the category, subcategory, and service of the new template.
#
# The script will create the required directories and files, as well as copy
# utility files to facilitate the template's usage. It will also ensure that
# the directory does not already exist to prevent accidental overwrites.
#
# Note: The user must provide valid inputs for category, subcategory, and service,
# and the specified directory must not already exist.
# --------------------------------------------------------------------------------


# Function to create the directory structure for a new template
create_template_structure() {

  # Directory path argument
  directory="$1"

  echo
  echo "Creating directory: templates/$directory"

  # ------------------
  # TEMPLATE STRUCTURE
  # ------------------
  # Creating directories and files for the new template
  mkdir -p templates/$directory/{hooks,docs,images,"{{ cookiecutter.project_slug }}"}/
  touch templates/$directory/{docs,images}/.gitkeep

  # Copying utility files
  cp utils/{pre,post}_gen_project.{sh,py} templates/$directory/hooks/
  cp utils/cookiecutter.json templates/$directory/
  cp utils/.gitignore templates/$directory/
  cp utils/.env.sample templates/$directory/

  # Create a README for the new template
  echo "# New template project" > templates/$directory/README.md


  # -----------------------
  # INNER PROJECT STRUCTURE
  # -----------------------
  # Creating directories and files for the inner project in the new template
  mkdir -p templates/$directory/"{{ cookiecutter.project_slug }}"/{scripts,docs,images}/
  touch templates/$directory/"{{ cookiecutter.project_slug }}"/{docs,images}/.gitkeep

  # Copy utility files into the inner project in the new template
  cp utils/{setup,cleanup,gcp_login}.sh templates/$directory/"{{ cookiecutter.project_slug }}"/scripts/
  cp utils/README.md templates/$directory/"{{ cookiecutter.project_slug }}"/
  cp utils/.gitignore templates/$directory/"{{ cookiecutter.project_slug }}"/
  cp utils/.env.sample templates/$directory/"{{ cookiecutter.project_slug }}"/


  echo
  echo WARNING:
  echo "Order of execution in 'templates/$directory/hooks/':"
  echo "1. pre_gen_project.py"
  echo "2. pre_gen_project.sh"
  echo "3. (Mount the template)"
  echo "4. post_gen_project.py"
  echo "5. post_gen_project.sh"

  echo
  echo WARNING:
  echo "Remember to add the configuration of the new template to the './cookiecutter.json' file"
  echo "$directory (./templates/$directory)"
}

# Prompting user for inputs
read -p "Enter category: " category
read -p "Enter subcategory: " subcategory
read -p "Enter service: " service

# Check if any of the required inputs is missing
if [ -z "$category" ] || [ -z "$subcategory" ] || [ -z "$service" ]; then
  echo "Error: Category, subcategory and service cannot be empty."
  exit 1
fi

directory="$category/$subcategory/$service"

# Check if the directory already exists
if [ -d "templates/$directory" ]; then
  echo "Directory already exists. Aborting."
  exit 1
fi

# Call the function to create the new template structure
create_template_structure $directory
