# Profiles

Types:

```python
from endex_factset_people.types import PeopleProfilesResponse
```

Methods:

- <code title="post /factset-people/v1/profiles">client.profiles.<a href="./src/endex_factset_people/resources/profiles.py">create</a>(\*\*<a href="src/endex_factset_people/types/profile_create_params.py">params</a>) -> <a href="./src/endex_factset_people/types/people_profiles_response.py">PeopleProfilesResponse</a></code>
- <code title="get /factset-people/v1/profiles">client.profiles.<a href="./src/endex_factset_people/resources/profiles.py">list</a>(\*\*<a href="src/endex_factset_people/types/profile_list_params.py">params</a>) -> <a href="./src/endex_factset_people/types/people_profiles_response.py">PeopleProfilesResponse</a></code>

# JobHistories

Types:

```python
from endex_factset_people.types import PeopleJobsResponse
```

Methods:

- <code title="post /factset-people/v1/jobs">client.job_histories.<a href="./src/endex_factset_people/resources/job_histories.py">create</a>(\*\*<a href="src/endex_factset_people/types/job_history_create_params.py">params</a>) -> <a href="./src/endex_factset_people/types/people_jobs_response.py">PeopleJobsResponse</a></code>
- <code title="get /factset-people/v1/jobs">client.job_histories.<a href="./src/endex_factset_people/resources/job_histories.py">list</a>(\*\*<a href="src/endex_factset_people/types/job_history_list_params.py">params</a>) -> <a href="./src/endex_factset_people/types/people_jobs_response.py">PeopleJobsResponse</a></code>

# Companies

## Executives

Types:

```python
from endex_factset_people.types.companies import CompanyPeopleResponse
```

Methods:

- <code title="post /factset-people/v1/company-people">client.companies.executives.<a href="./src/endex_factset_people/resources/companies/executives.py">create</a>(\*\*<a href="src/endex_factset_people/types/companies/executive_create_params.py">params</a>) -> <a href="./src/endex_factset_people/types/companies/company_people_response.py">CompanyPeopleResponse</a></code>
- <code title="get /factset-people/v1/company-people">client.companies.executives.<a href="./src/endex_factset_people/resources/companies/executives.py">list</a>(\*\*<a href="src/endex_factset_people/types/companies/executive_list_params.py">params</a>) -> <a href="./src/endex_factset_people/types/companies/company_people_response.py">CompanyPeopleResponse</a></code>

## Positions

Types:

```python
from endex_factset_people.types.companies import CompanyPositionsResponse
```

Methods:

- <code title="post /factset-people/v1/company-positions">client.companies.positions.<a href="./src/endex_factset_people/resources/companies/positions.py">create</a>(\*\*<a href="src/endex_factset_people/types/companies/position_create_params.py">params</a>) -> <a href="./src/endex_factset_people/types/companies/company_positions_response.py">CompanyPositionsResponse</a></code>
- <code title="get /factset-people/v1/company-positions">client.companies.positions.<a href="./src/endex_factset_people/resources/companies/positions.py">list</a>(\*\*<a href="src/endex_factset_people/types/companies/position_list_params.py">params</a>) -> <a href="./src/endex_factset_people/types/companies/company_positions_response.py">CompanyPositionsResponse</a></code>

## Compensations

Types:

```python
from endex_factset_people.types.companies import CompanyCompensationResponse
```

Methods:

- <code title="post /factset-people/v1/company-compensation">client.companies.compensations.<a href="./src/endex_factset_people/resources/companies/compensations.py">create</a>(\*\*<a href="src/endex_factset_people/types/companies/compensation_create_params.py">params</a>) -> <a href="./src/endex_factset_people/types/companies/company_compensation_response.py">CompanyCompensationResponse</a></code>
- <code title="get /factset-people/v1/company-compensation">client.companies.compensations.<a href="./src/endex_factset_people/resources/companies/compensations.py">list</a>(\*\*<a href="src/endex_factset_people/types/companies/compensation_list_params.py">params</a>) -> <a href="./src/endex_factset_people/types/companies/company_compensation_response.py">CompanyCompensationResponse</a></code>

# CompanyStats

Types:

```python
from endex_factset_people.types import CompanyStatsResponse
```

Methods:

- <code title="post /factset-people/v1/company-stats">client.company_stats.<a href="./src/endex_factset_people/resources/company_stats.py">create</a>(\*\*<a href="src/endex_factset_people/types/company_stat_create_params.py">params</a>) -> <a href="./src/endex_factset_people/types/company_stats_response.py">CompanyStatsResponse</a></code>
- <code title="get /factset-people/v1/company-stats">client.company_stats.<a href="./src/endex_factset_people/resources/company_stats.py">retrieve</a>(\*\*<a href="src/endex_factset_people/types/company_stat_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_people/types/company_stats_response.py">CompanyStatsResponse</a></code>
