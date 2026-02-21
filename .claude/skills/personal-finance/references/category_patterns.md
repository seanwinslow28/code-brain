# Categorization Regex Patterns

Use these regex patterns to strictly classify transaction descriptions. Order matters (process specific before generic).

## Income
| Pattern (Regex) | Matches |
| :--- | :--- |
| `r'payroll|direct\s?dep|gusto|adp|salary'` | Payroll, Direct Deposit |
| `r'interest|dividend|schwab\s?brokerage'` | Bank Interest, Dividends |

## Essential Fixed
| Pattern (Regex) | Matches |
| :--- | :--- |
| `r'rent|mortgage|lease|property\s?mgt'` | Rent payment |
| `r'con\s?ed|utilities|water\s?dept|electric'` | Utilities |
| `r'verizon|at&t|t-mobile|xfinity|internet'` | Internet/Phone |
| `r'geico|state\s?farm|progressive|insurance'` | Insurance |

## Transport
| Pattern (Regex) | Matches |
| :--- | :--- |
| `r'uber|lyft|ride|taxi'` | Rideshare |
| `r'mta|subway|metro|transit|clipper'` | Public Transit |
| `r'shell|bp|exxon|mobil|gas|fuel'` | Gas Stations |
| `r'parking|garage|meter'` | Parking |

## Food & Dining
| Pattern (Regex) | Matches |
| :--- | :--- |
| `r'whole\s?fds|trader\s?joes|safeway|kroger|aldi|wegmans'` | Groceries |
| `r'doordash|ubereats|grubhub|seamless|caviar'` | Food Delivery |
| `r'starbucks|peet|coffee|blue\s?bottle|dunkin'` | Coffee |
| `r'chipotle|sweetgreen|cava|shake\s?shack|restaurant|cafe|bar|pub'` | Dining Out |

## Shopping & Lifestyle
| Pattern (Regex) | Matches |
| :--- | :--- |
| `r'amazon|amzn|prime'` | Amazon |
| `r'apple|itunes|app\s?store'` | Apple/Tech |
| `r'cvs|walgreens|rite\s?aid|duane\s?reade'` | Pharmacy |
| `r'target|walmart|costco'` | General Retail |
| `r'uniqlo|zara|nike|adidas|clothing'` | Clothing |

## Subscriptions & Software
| Pattern (Regex) | Matches |
| :--- | :--- |
| `r'netflix|hulu|hbo|disney|spotify|youtube'` | Entertainment |
| `r'aws|google\s?cloud|azure|github|digitalocean|heroku'` | Cloud/Dev |
| `r'notion|obsidian|roam|linear|slack|zoom'` | Productivity |
| `r'nyt|wsj|substack|medium|bloomberg'` | News |

## Health
| Pattern (Regex) | Matches |
| :--- | :--- |
| `r'gym|equinox|planet fit|fitness'` | Gym |
| `r'doctor|dental|medical|hospital'` | Medical |
| `r'therapy|counseling|psych'` | Mental Health |
