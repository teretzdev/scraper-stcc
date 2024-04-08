const fs = require('fs');
const pdfParse = require('pdf-parse');
const xlsx = require('xlsx');

const pdfFilePath = 'stcc_raw_data.pdf'; // Adjust this to the correct PDF file path

const extractDataFromPDF = async (pdfPath) => {
    console.log(`Reading PDF file from path: ${pdfPath}`);
    const dataBuffer = fs.readFileSync(pdfPath);

    try {
        console.log(`Starting PDF parsing`);
        const data = await pdfParse(dataBuffer);
        console.log(`PDF parsing completed`);

        const lines = data.text.split('\n');
        console.log(`Total lines extracted from PDF: ${lines.length}`);

        const entries = [];
        let currentRecord = {};

        lines.forEach((line, index) => {
            line = line.trim();
            console.log(`Processing line ${index + 1}: ${line}`);

            const dateMatches = line.match(/\d{2}\/\d{2}\/\d{2}/g);
            if (dateMatches) {
                if (Object.keys(currentRecord).length) {
                    entries.push(currentRecord);
                    console.log(`Record completed and pushed: `, currentRecord);
                    currentRecord = {};
                }
                currentRecord.bookDate = dateMatches[0];
                currentRecord.releaseDate = dateMatches[1] || 'Not Available';
                console.log(`Dates found - Book Date: ${currentRecord.bookDate}, Release Date: ${currentRecord.releaseDate}`);
            }

            const nameMatch = line.match(/^[A-Z]+,\s[A-Z]+/);
            if (nameMatch) {
                const names = nameMatch[0].split(',');
                currentRecord.lastName = names[0].trim();
                const firstMiddle = names[1].trim().split(' ');
                currentRecord.firstName = firstMiddle.shift();
                currentRecord.middleName = firstMiddle.join(' ') || 'Not Available';
                console.log(`Name found - Last Name: ${currentRecord.lastName}, First Name: ${currentRecord.firstName}, Middle Name: ${currentRecord.middleName}`);
            }

            const offenseMatch = line.match(/^[A-Z0-9].* - .*$/);
            if (offenseMatch) {
                currentRecord.offenses = line;
                console.log(`Offense found: ${line}`);
            }

            if (index > 0 && lines[index - 1].match(/^[A-Z]+,\s[A-Z]+/) && !dateMatches && !offenseMatch) {
                if (currentRecord.address) {
                    currentRecord.address += " " + line;
                } else {
                    currentRecord.address = line;
                }
                console.log(`Address line appended: ${line}`);
            }
        });

        if (Object.keys(currentRecord).length) {
            entries.push(currentRecord);
            console.log(`Final record pushed: `, currentRecord);
        }

        console.log(`Total records processed: ${entries.length}`);

        const transformedEntries = entries.map(entry => ({
            LastName: entry.lastName || '',
            FirstName: entry.firstName || '',
            Address: entry.address || '',
            City: '', // Placeholder for City, as extraction logic is not defined
            State: '', // Placeholder for State, as extraction logic is not defined
            Zip: '', // Placeholder for Zip, as extraction logic is not defined
            Offense: entry.offenses || '',
            BookDate: entry.bookDate || '',
            ReleaseDate: entry.releaseDate || '',
        }));

        const worksheet = xlsx.utils.json_to_sheet(transformedEntries);
        const workbook = xlsx.utils.book_new();
        xlsx.utils.book_append_sheet(workbook, worksheet, 'Inmates');
        xlsx.writeFile(workbook, 'InmateRecords.xlsx');
        console.log('Excel file written successfully.');
    } catch (error) {
        console.error('Error processing PDF:', error);
    }
};

extractDataFromPDF(pdfFilePath);
