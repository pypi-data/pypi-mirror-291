// sphinxcontrib_rust - Sphinx extension for the Rust programming language
// Copyright (C) 2024  Munir Contractor
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

//! Module for various utility classes and structs

use std::fs::read_to_string;
use std::path::{Path, PathBuf};

use cargo_toml::Manifest;

/// Check the provided paths for the Cargo.toml file.
///
/// Returns:
///     A Some value of the path that contained the Cargo manifest and the
///     associated manifest for the first path contains a ``Cargo.toml`` file.
pub(crate) fn check_for_manifest(paths: Vec<&Path>) -> Option<(PathBuf, CargoManifest)> {
    for path in paths {
        let manifest_path = path.join("Cargo.toml");
        if manifest_path.is_file() {
            return Some((
                path.into(),
                CargoManifest(Manifest::from_path(manifest_path).unwrap()),
            ));
        }
    }
    None
}

/// Struct for the source code files encountered when scanning the crate.
#[derive(Clone, Debug)]
pub(crate) struct SourceCodeFile {
    /// The path to the file.
    pub(crate) path: PathBuf,
    /// The name of the item in the file.
    pub(crate) item: String,
}

impl SourceCodeFile {
    pub(crate) fn ast(&self) -> syn::File {
        syn::parse_file(&read_to_string(&self.path).unwrap()).unwrap()
    }

    pub(crate) fn to_parent_directory(&self) -> Self {
        SourceCodeFile {
            path: self.path.parent().as_ref().unwrap().into(),
            item: self.item.clone(),
        }
    }
}

/// Newtype struct for the Cargo manifest from cargo_toml
pub(crate) struct CargoManifest(Manifest);

impl CargoManifest {
    /// Get the library file for the crate, if any.
    pub(crate) fn lib_file(&self, crate_dir: &Path) -> Option<SourceCodeFile> {
        self.0.lib.as_ref().map(|lib| {
            let path = crate_dir.join(lib.path.as_ref().unwrap());
            SourceCodeFile {
                path,
                item: lib.name.as_ref().unwrap().clone(),
            }
        })
    }

    /// Get all the executable files in the crate.
    pub(crate) fn executable_files(&self, crate_dir: &Path) -> Vec<SourceCodeFile> {
        self.0
            .bin
            .iter()
            .map(|prd| {
                let bin_path = crate_dir.join(prd.path.as_ref().unwrap());
                SourceCodeFile {
                    path: bin_path,
                    item: prd.name.as_ref().unwrap().clone(),
                }
            })
            .collect()
    }
}
