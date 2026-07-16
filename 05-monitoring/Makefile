run:
	python assistant.py

chat:
	streamlit run app.py

network:
	docker network create monitoring

postgres:
	docker run -it --name course-assistant-pg --network monitoring -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=course_assistant -p 5432:5432 -v pgdata:/var/lib/postgresql/data postgres:17

# streamlit run dashboard.py --server.port 8502