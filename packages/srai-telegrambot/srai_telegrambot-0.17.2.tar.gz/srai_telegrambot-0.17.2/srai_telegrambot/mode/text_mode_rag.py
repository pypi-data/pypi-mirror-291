import base64
import os
import pickle as pkl

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import VectorStore

# from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from srai_telegrambot.mode.text_mode_base import TextModeBase


class TextModeRag(TextModeBase):

    def __init__(self, path_dir_vectorstore: str):
        super().__init__("text_mode_rag")
        self.path_dir_vectorstore = path_dir_vectorstore
        if not os.path.exists(self.path_dir_vectorstore):
            os.makedirs(self.path_dir_vectorstore)

        self.list_path_file_pdf = []
        self.list_path_file_txt = []
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        # Create vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore: VectorStore = None  # type: ignore
        if not os.path.isfile(os.path.join(path_dir_vectorstore, "index.pkl")):
            self.rebuild_vectorstore()
        else:
            raise Exception("FAISS is not supported in this version of the library")
            # self.vectorstore = FAISS.load_local(
            #     path_dir_vectorstore,
            #     embeddings=embeddings,
            #     allow_dangerous_deserialization=True,
            # )
        # Create conversation chain
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-4")

    def rebuild_vectorstore(self):
        list_page = []
        for path_file in self.list_path_file_pdf:
            loader = PyPDFLoader(file_path=path_file)
            list_page.extend(loader.load_and_split(self.text_splitter))
        for path_file in self.list_path_file_txt:
            loader = TextLoader(file_path=path_file)
            list_page.extend(loader.load_and_split(self.text_splitter))

        # self.vectorstore = FAISS.from_documents(list_page, embedding=OpenAIEmbeddings())
        # self.vectorstore.save_local(self.path_dir_vectorstore)
        raise Exception("FAISS is not supported in this version of the library")

    def add_path_file_pdf(self, path_file: str):
        self.list_path_file_pdf.append(path_file)

    def add_path_file_txt(self, path_file: str):
        self.list_path_file_txt.append(path_file)

    def _handle_text(self, chat_id: str, prompt: str) -> str:
        mode_state = self.try_load_mode_state(chat_id)
        if mode_state is None:
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        else:
            memory_string = mode_state["memory_string"]
            memory = pkl.loads(base64.b64decode(memory_string))

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm, chain_type="stuff", retriever=self.vectorstore.as_retriever(), memory=memory
        )

        result = conversation_chain.invoke({"question": prompt})

        memory_string = base64.b64encode(pkl.dumps(memory)).decode("utf-8")
        mode_state = {"memory_string": memory_string}
        self.save_mode_state(chat_id, mode_state)
        return result["answer"]
        return result["answer"]
        return result["answer"]
