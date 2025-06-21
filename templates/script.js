function showPage(pageId) {
            document.getElementById('homePage').classList.add('hidden');
            document.getElementById('predictPage').classList.add('hidden');
            document.getElementById(pageId + 'Page').classList.remove('hidden');
            // Hide result container when switching pages
            resultContainer.classList.add('hidden', 'scale-95', 'opacity-0');
            resultContainer.classList.remove('scale-100', 'opacity-100', 'translucent-success', 'border-limeGreen', 'translucent-danger', 'border-dangerRed');
        }

        // Initialize to home page
        document.addEventListener('DOMContentLoaded', () => {
            showPage('home');
        });

        // Function to display custom messages
        function showMessageBox(title, content) {
            document.getElementById('messageBoxTitle').textContent = title;
            document.getElementById('messageBoxContent').textContent = content;
            document.getElementById('messageBox').classList.remove('hidden');
        }

        // Close message box
        document.getElementById('messageBoxClose').addEventListener('click', function() {
            document.getElementById('messageBox').classList.add('hidden');
        });

        // Get form and result elements (moved to be accessible by event listeners)
        const form = document.getElementById('creditApplicationForm');
        const resultContainer = document.getElementById('resultContainer');
        const resultTitle = document.getElementById('resultTitle');
        const resultDetails = document.getElementById('resultDetails');
        const closeResultButton = document.getElementById('closeResultButton');
        const resetButton = document.getElementById('resetButton');

        // Event listener for form submission
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission

            // --- 1. Gather Form Data ---
            const formData = {
                fullName: document.getElementById('fullName').value.trim(),
                email: document.getElementById('email').value.trim(),
                age: parseInt(document.getElementById('age').value),
                dependents: parseInt(document.getElementById('dependents').value),
                income: parseFloat(document.getElementById('income').value),
                creditScore: parseInt(document.getElementById('creditScore').value),
                monthlyDebt: parseFloat(document.getElementById('monthlyDebt').value),
                employmentStatus: document.getElementById('employmentStatus').value,
                employmentYears: parseInt(document.getElementById('employmentYears').value),
                housingStatus: document.getElementById('housingStatus').value,
                monthlyHousingCost: parseFloat(document.getElementById('monthlyHousingCost').value),
                hasStudentLoan: document.getElementById('hasStudentLoan').checked,
                hasAutoLoan: document.getElementById('hasAutoLoan').checked,
                hasMortgage: document.getElementById('hasMortgage').checked,
                loanHistoryCount: parseInt(document.getElementById('loanHistoryCount').value)
            };

            // --- 2. Input Validation (Client-side) ---
            if (!formData.fullName || !formData.email || !formData.age || !formData.income ||
                !formData.creditScore || !formData.employmentStatus || !formData.housingStatus) {
                showMessageBox('Input Error', 'Please fill in all required fields.');
                return;
            }

            if (formData.age < 18 || formData.age > 100) {
                showMessageBox('Input Error', 'Age must be between 18 and 100.');
                return;
            }
            if (formData.creditScore < 300 || formData.creditScore > 850) {
                showMessageBox('Input Error', 'Credit Score must be between 300 and 850.');
                return;
            }
            if (formData.income <= 0) {
                 showMessageBox('Input Error', 'Annual Income must be greater than zero.');
                 return;
            }
            if (formData.monthlyDebt < 0 || formData.monthlyHousingCost < 0 || formData.loanHistoryCount < 0 || formData.dependents < 0 || formData.employmentYears < 0) {
                showMessageBox('Input Error', 'Numeric fields cannot be negative.');
                return;
            }


            // --- 3. Simulated Credit Card Approval Logic (Replaces ML Model Call) ---
            // This is a comprehensive rule-based system mimicking a complex ML model's decisions.
            // In a real application, you would send `formData` to your backend ML model API.

            let approved = false;
            let rejectionReason = "No specific reason identified."; // Default reason

            // Calculate Debt-to-Income Ratio (DTI)
            // Includes monthly debt payments + monthly housing cost
            const totalMonthlyOutgo = formData.monthlyDebt + formData.monthlyHousingCost;
            const monthlyIncome = formData.income / 12;
            let dti = 0;
            if (monthlyIncome > 0) {
                dti = totalMonthlyOutgo / monthlyIncome;
            } else {
                rejectionReason = "Monthly income cannot be zero for DTI calculation.";
                approved = false; // Cannot approve if no income for DTI
            }

            // Define thresholds for various factors
            const MIN_CREDIT_SCORE_GOOD = 700;
            const MIN_CREDIT_SCORE_FAIR = 600;
            const MIN_INCOME_HIGH = 75000;
            const MIN_INCOME_MODERATE = 40000;
            const MAX_DTI_ACCEPTABLE = 0.43; // Generally, 43% is the max for many lenders
            const MAX_DTI_RISKY = 0.50;
            const MIN_EMPLOYMENT_YEARS_STABLE = 2;

            let approvalScore = 0; // A simple scoring system for nuanced decisions

            // Score based on Credit Score
            if (formData.creditScore >= MIN_CREDIT_SCORE_GOOD) {
                approvalScore += 3; // Excellent
            } else if (formData.creditScore >= MIN_CREDIT_SCORE_FAIR) {
                approvalScore += 2; // Good
            } else if (formData.creditScore >= 500) {
                approvalScore += 1; // Fair
            } else {
                rejectionReason = "Credit score is too low.";
            }

            // Score based on Income
            if (formData.income >= MIN_INCOME_HIGH) {
                approvalScore += 3;
            } else if (formData.income >= MIN_INCOME_MODERATE) {
                approvalScore += 2;
            } else if (formData.income >= 25000) {
                approvalScore += 1;
            } else {
                rejectionReason = "Income is insufficient.";
            }

            // Score based on DTI
            if (dti <= MAX_DTI_ACCEPTABLE && monthlyIncome > 0) {
                approvalScore += 3;
            } else if (dti <= MAX_DTI_RISKY && monthlyIncome > 0) {
                approvalScore += 1;
            } else if (monthlyIncome > 0) {
                rejectionReason = "Debt-to-Income ratio is too high.";
            }

            // Score based on Employment Status and Years
            if (formData.employmentStatus === 'employed' || formData.employmentStatus === 'selfEmployed') {
                if (formData.employmentYears >= MIN_EMPLOYMENT_YEARS_STABLE) {
                    approvalScore += 2; // Stable employment
                } else {
                    approvalScore += 1; // Employed but less stable
                }
            } else if (formData.employmentStatus === 'retired' || formData.employmentStatus === 'student') {
                // Retired/Student can be approved if other factors are strong (e.g., high credit score, low DTI, assets)
                // We won't add negative score but won't add high positive score based on this alone
                rejectionReason = "Employment status is not 'Employed' or 'Self-Employed' and other factors are not strong enough.";
                // This will be overridden if overall score is high
            } else { // Unemployed
                rejectionReason = "Applicant is unemployed.";
            }

            // Score based on Loan History
            if (formData.loanHistoryCount === 0 && !formData.hasStudentLoan && !formData.hasAutoLoan && !formData.hasMortgage) {
                approvalScore += 1; // Clean slate
            } else if (formData.loanHistoryCount <= 2 && !formData.hasAutoLoan) {
                approvalScore += 0.5; // Manageable loans
            } else if (formData.loanHistoryCount > 3 || formData.hasStudentLoan || formData.hasAutoLoan) {
                // Having multiple loans or specific loan types might slightly reduce score unless compensated
            }

            // Overall decision logic based on approvalScore and critical flags
            if (formData.creditScore < 550) { // Hard rejection minimum
                approved = false;
                rejectionReason = "Your credit score is too low.";
            } else if (monthlyIncome === 0 || dti > 0.6) { // Critical financial flags
                 approved = false;
                 rejectionReason = "Income is zero or Debt-to-Income ratio is critically high.";
            } else if (formData.employmentStatus === 'unemployed' && formData.income < 10000) { // Low income + unemployed
                approved = false;
                rejectionReason = "Applicant is unemployed with insufficient income.";
            } else if (formData.age < 21 && formData.income < 30000) { // Younger applicants with lower income
                approved = false;
                rejectionReason = "Applicant is young with limited income, indicating higher risk.";
            }
             else if (approvalScore >= 7) { // Strong approval criteria
                approved = true;
                rejectionReason = "Congratulations! Your profile meets our high approval criteria.";
            } else if (approvalScore >= 4 && formData.creditScore >= 600) { // Moderate approval criteria
                approved = true;
                rejectionReason = "Your application is approved based on a balanced profile.";
            } else { // Default to rejection if not explicitly approved
                approved = false;
                if (rejectionReason === "No specific reason identified.") {
                    rejectionReason = "Your current profile does not meet our credit eligibility criteria. Factors such as income, credit history, or existing debt may need improvement.";
                }
            }


            // --- 4. Display Results ---
            resultContainer.classList.remove('hidden');
            // Animate result container
            setTimeout(() => {
                resultContainer.classList.remove('scale-95', 'opacity-0');
                resultContainer.classList.add('scale-100', 'opacity-100');
            }, 10); // Small delay for animation

            // Remove existing translucent classes
            resultContainer.classList.remove('translucent-success', 'translucent-danger');

            if (approved) {
                resultContainer.classList.remove('bg-red-100', 'border-dangerRed');
                resultContainer.classList.add('translucent-success', 'border-limeGreen'); // Use translucent and lime green border
                resultTitle.textContent = 'Application Approved!'; // No emojis
                resultTitle.classList.remove('text-dangerRed');
                resultTitle.classList.add('text-darkGreen'); // Use dark green for title
                resultDetails.innerHTML = `
                    <p class="text-neutralGray">Congratulations, ${formData.fullName}! Your application has been approved.</p>
                    <p class="text-sm text-gray-700 mt-2">${rejectionReason}</p>
                `;
            } else {
                resultContainer.classList.remove('bg-green-100', 'border-primaryGreen');
                resultContainer.classList.add('translucent-danger', 'border-dangerRed'); // Use translucent and danger red border
                resultTitle.textContent = 'Application Denied'; // No emojis
                resultTitle.classList.remove('text-primaryGreen');
                resultTitle.classList.add('text-dangerRed');
                resultDetails.innerHTML = `
                    <p class="text-neutralGray">We regret to inform you that your application for a credit card has been denied at this time.</p>
                    <p class="text-sm text-gray-700 mt-2">Reason: ${rejectionReason}</p>
                    <p class="text-sm text-gray-700 mt-2">We encourage you to review your financial profile and try again in the future.</p>
                `;
            }

            // Scroll to result for better UX on smaller screens
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });

        // Event listener for closing the result container
        closeResultButton.addEventListener('click', function() {
            resultContainer.classList.add('scale-95', 'opacity-0');
            resultContainer.classList.remove('scale-100', 'opacity-100');
            setTimeout(() => {
                resultContainer.classList.add('hidden');
            }, 500); // Match transition duration
        });

        // Event listener for reset button
        resetButton.addEventListener('click', function() {
            form.reset(); // Reset form fields
            resultContainer.classList.add('hidden', 'scale-95', 'opacity-0'); // Hide and reset result display
            resultContainer.classList.remove('scale-100', 'opacity-100', 'translucent-success', 'border-limeGreen', 'translucent-danger', 'border-dangerRed');
            resultTitle.textContent = '';
            resultDetails.innerHTML = '';
        });

        // Optional: Smooth scroll to top on page load for consistent view
        window.addEventListener('load', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });