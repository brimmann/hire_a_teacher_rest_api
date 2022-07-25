import pickle

from hire_a_teacher_rest_api import settings

data = {
    "title": "Math Teacher",
    "status": "active",
    "exp_level": "Entry",
    "type": "Full-time",
    "city": "Islamabad",
    "date_posted": "1658593709044",
    "expire_date": "2022/07/28",
    "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab accusantium autem cum cupiditate deserunt est eum, fugit inventore iure minima minus mollitia nam non nulla omnis perspiciatis provident quae quidem quis reprehenderit sunt ut veniam voluptates? Porro, sunt, voluptates? Ad atque aut autem consequuntur, corporis deserunt distinctio doloremque dolores ducimus ea eos et ex fugit in itaque labore libero magni minima minus modi molestiae mollitia neque non nulla officiis pariatur quae quam, quia quibusdam quidem quo recusandae repellendus repudiandae sint sit vel vero! Ab adipisci at cupiditate delectus doloribus hic in minima, minus modi quasi qui sunt totam voluptate voluptatem.",
    "tags": "MATH,SCHOOL,TEACHER,PART",
    "apps_no": 0
}

with open(f'{settings.BASE_DIR}/jobs/test.pkl', 'wb') as file:
    pickle.dump(data, file)

with open(f'{settings.BASE_DIR}/jobs/test.pkl', 'rb') as file:
    data2 = pickle.load(file)

print(data2)

