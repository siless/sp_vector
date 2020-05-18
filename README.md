# sp_vector
Converter for sp_vector data to json

 <https://www.space-track.org> promotes space flight safety, protection of the space environment and the peaceful use of 
 space worldwide by sharing space situational awareness services and information with U.S. and international satellite owners/operators, academia and other entities.
 
 They offer sp_vector data as a *tar.gz with plain text files. Using these data in a proper way, it is crucial to 
 transform them to json.
 
Usage:
-   download the repo from git
-   download the vectors_<number>.tar.gz from space-track
-   copy the archive to src-folder
-   run "python3 start.py <archive.tar.gz>"
-   converted data will be stored to sp_vector.json