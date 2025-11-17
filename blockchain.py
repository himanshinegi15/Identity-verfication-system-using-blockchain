import hashlib, time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data="Genesis Block")

    def create_block(self, data):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.ctime(),
            'data': data,
            'prev_hash': self.chain[-1]['hash'] if self.chain else '0',
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def hash(self, block):
        text = str(block['data']) + block['prev_hash']
        return hashlib.sha256(text.encode()).hexdigest()

    def add_block(self, data):
        return self.create_block(data)
